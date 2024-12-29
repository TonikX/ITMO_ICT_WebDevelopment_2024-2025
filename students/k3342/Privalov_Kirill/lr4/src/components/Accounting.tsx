import React, { useEffect, useState } from "react";
import {
  Container,
  Typography,
  Box,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import api from "../api/api";

interface IService {
  serviceId?: number;
  name: string;
  description?: string;
  serviceType?: string;
}

interface IServicePrice {
  servicePriceId?: number;
  serviceId: number;
  service?: IService;
  price: string; // Changed from number to string to match API response
  validFrom: string;
  validTo?: string;
}

const Accounting: React.FC = () => {
  const [services, setServices] = useState<IService[]>([]);
  const [openServiceDialog, setOpenServiceDialog] = useState(false);
  const [currentService, setCurrentService] = useState<IService | null>(null);
  const [serviceForm, setServiceForm] = useState<IService>({
    name: "",
    description: "",
    serviceType: "",
  });
  const [priceError, setPriceError] = useState<string>("");
  const [servicePrices, setServicePrices] = useState<IServicePrice[]>([]);
  const [openPriceDialog, setOpenPriceDialog] = useState(false);
  const [currentPrice, setCurrentPrice] = useState<IServicePrice | null>(null);
  const [priceForm, setPriceForm] = useState<IServicePrice>({
    serviceId: 0,
    price: "0",
    validFrom: "",
    validTo: "",
  });

  useEffect(() => {
    fetchServices();
    fetchServicePrices();
  }, []);

  const fetchServices = async () => {
    try {
      const response = await api.get<IService[]>("/services/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      });
      setServices(response.data);
    } catch (error) {
      console.error("Error fetching services:", error);
    }
  };

  const handleSubmitService = async () => {
    try {
      if (currentService?.serviceId) {
        await api.put(
          `/services/${currentService.serviceId}/`,
          serviceForm,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
          }
        );
      } else {
        await api.post("/services/", serviceForm, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        });
      }
      fetchServices();
      handleCloseServiceDialog();
    } catch (error) {
      console.error("Error submitting service:", error);
    }
  };

  const handleDeleteService = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this service?")) {
      try {
        await api.delete(`/services/${id}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        });
        fetchServices();
      } catch (error) {
        console.error("Error deleting service:", error);
      }
    }
  };

  const handleOpenServiceDialog = (service?: IService) => {
    if (service) {
      setCurrentService(service);
      setServiceForm(service);
    } else {
      setCurrentService(null);
      setServiceForm({ name: "", description: "", serviceType: "" });
    }
    setOpenServiceDialog(true);
  };

  const handleCloseServiceDialog = () => {
    setOpenServiceDialog(false);
    setCurrentService(null);
    setServiceForm({ name: "", description: "", serviceType: "" });
  };

  const fetchServicePrices = async () => {
    try {
      const response = await api.get<IServicePrice[]>(
        "/serviceprices/",
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        }
      );
      setServicePrices(response.data);
    } catch (error) {
      console.error("Error fetching service prices:", error);
    }
  };

  const handleSubmitPrice = async () => {
    const today = new Date().setHours(0, 0, 0, 0);
    const validFromDate = new Date(priceForm.validFrom).setHours(0, 0, 0, 0);

    if (validFromDate < today) {
      setPriceError("Valid From date cannot be before today.");
      return;
    }
    setPriceError("");
    try {
      if (currentPrice?.servicePriceId) {
        await api.put(
          `/serviceprices/${currentPrice.servicePriceId}/`,
          { ...priceForm, price: priceForm.price },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
          }
        );
      } else {
        await api.post(
          "/serviceprices/",
          { ...priceForm, price: priceForm.price },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
          }
        );
      }
      fetchServicePrices();
      handleClosePriceDialog();
    } catch (error) {
      console.error("Error submitting service price:", error);
    }
  };

  const handleDeletePrice = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this price?")) {
      try {
        await api.delete(`/serviceprices/${id}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        });
        fetchServicePrices();
      } catch (error) {
        console.error("Error deleting service price:", error);
      }
    }
  };

  const handleOpenPriceDialog = (price?: IServicePrice) => {
    if (price) {
      setCurrentPrice(price);
      setPriceForm({ ...price, price: price.price });
    } else {
      setCurrentPrice(null);
      setPriceForm({ serviceId: 0, price: "0", validFrom: "", validTo: "" });
    }
    setOpenPriceDialog(true);
  };

  const handleClosePriceDialog = () => {
    setOpenPriceDialog(false);
    setCurrentPrice(null);
    setPriceForm({ serviceId: 0, price: "0", validFrom: "", validTo: "" });
    setPriceError("");
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Accounting Management
      </Typography>

      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", mb: 2 }}>
          <Typography variant="h6">Services</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => handleOpenServiceDialog()}
          >
            Add Service
          </Button>
        </Box>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {services.map((service) => (
                <TableRow key={service.serviceId}>
                  <TableCell>{service.name}</TableCell>
                  <TableCell>{service.serviceType || "N/A"}</TableCell>
                  <TableCell>{service.description || "N/A"}</TableCell>
                  <TableCell>
                    <Button
                      onClick={() => handleOpenServiceDialog(service)}
                      variant="outlined"
                      sx={{ mr: 1 }}
                    >
                      Edit
                    </Button>
                    <Button
                      onClick={() => handleDeleteService(service.serviceId!)}
                      variant="outlined"
                      color="error"
                    >
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>

      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", mb: 2 }}>
          <Typography variant="h6">Service Prices</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => handleOpenPriceDialog()}
          >
            Add Price
          </Button>
        </Box>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Service</TableCell>
                <TableCell>Price</TableCell>
                <TableCell>Valid From</TableCell>
                <TableCell>Valid To</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {servicePrices.map((price) => (
                <TableRow key={price.servicePriceId}>
                  <TableCell>
                    {services.find((s) => s.serviceId === price.serviceId)?.name || "N/A"}
                  </TableCell>
                  <TableCell>{price.price}</TableCell>
                  <TableCell>{price.validFrom}</TableCell>
                  <TableCell>{price.validTo || "N/A"}</TableCell>
                  <TableCell>
                    <Button
                      onClick={() => handleOpenPriceDialog(price)}
                      variant="outlined"
                      sx={{ mr: 1 }}
                    >
                      Edit
                    </Button>
                    <Button
                      onClick={() => handleDeletePrice(price.servicePriceId!)}
                      variant="outlined"
                      color="error"
                    >
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>

      <Dialog open={openServiceDialog} onClose={handleCloseServiceDialog}>
        <DialogTitle>
          {currentService ? "Edit Service" : "Add Service"}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
            <TextField
              label="Service Name"
              value={serviceForm.name}
              onChange={(e) =>
                setServiceForm({ ...serviceForm, name: e.target.value })
              }
              fullWidth
              required
            />
            <TextField
              label="Service Type"
              value={serviceForm.serviceType}
              onChange={(e) =>
                setServiceForm({ ...serviceForm, serviceType: e.target.value })
              }
              fullWidth
            />
            <TextField
              label="Description"
              value={serviceForm.description}
              onChange={(e) =>
                setServiceForm({ ...serviceForm, description: e.target.value })
              }
              fullWidth
              multiline
              rows={3}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseServiceDialog}>Cancel</Button>
          <Button
            onClick={handleSubmitService}
            variant="contained"
            color="primary"
          >
            {currentService ? "Update" : "Add"}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openPriceDialog} onClose={handleClosePriceDialog}>
        <DialogTitle>
          {currentPrice ? "Edit Service Price" : "Add Service Price"}
        </DialogTitle>
        <DialogContent>
          {priceError && <Typography color="error">{priceError}</Typography>}
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
            <FormControl fullWidth required>
              <InputLabel>Service</InputLabel>
              <Select
                value={priceForm.serviceId}
                onChange={(e) =>
                  setPriceForm({
                    ...priceForm,
                    serviceId: Number(e.target.value),
                  })
                }
                label="Service"
              >
                {services.map((service) => (
                  <MenuItem key={service.serviceId} value={service.serviceId}>
                    {service.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              label="Price"
              type="text" // Changed to text to accommodate decimal values as strings
              value={priceForm.price}
              onChange={(e) =>
                setPriceForm({ ...priceForm, price: e.target.value })
              }
              fullWidth
              required
              inputProps={{ pattern: "^[0-9]+(\\.[0-9]{1,2})?$" }}
              helperText="Enter a valid price (e.g., 1000.00)"
            />
            <TextField
              label="Valid From"
              type="date"
              value={priceForm.validFrom}
              onChange={(e) =>
                setPriceForm({ ...priceForm, validFrom: e.target.value })
              }
              fullWidth
              required
              InputLabelProps={{ shrink: true }}
            />
            <TextField
              label="Valid To"
              type="date"
              value={priceForm.validTo}
              onChange={(e) =>
                setPriceForm({ ...priceForm, validTo: e.target.value })
              }
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClosePriceDialog}>Cancel</Button>
          <Button
            onClick={handleSubmitPrice}
            variant="contained"
            color="primary"
          >
            {currentPrice ? "Update" : "Add"}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Accounting;