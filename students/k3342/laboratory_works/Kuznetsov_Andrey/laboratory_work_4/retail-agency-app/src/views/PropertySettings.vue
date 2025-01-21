<template>
    <div>
      <HeaderLoader :currentPath="currentPath" />
      
      <main role="main" class="container">
        <section class="property-settings">
          <h2>Add New Property</h2>
          
          <form @submit.prevent="addProperty">
            <div class="form-group">
              <label for="description">Description</label>
              <textarea id="description" v-model="newProperty.description" required></textarea>
            </div>
  
            <div class="form-group">
              <label for="propertyType">Property Type</label>
              <select id="propertyType" v-model="newProperty.propertyType" required>
                <option value="Apartment">Apartment</option>
                <option value="House">House</option>
                <option value="Villa">Villa</option>
              </select>
            </div>
  
            <div class="form-group">
              <label for="transactionType">Transaction Type</label>
              <select id="transactionType" v-model="newProperty.transactionType" required>
                <option value="Rent">Rent</option>
                <option value="Sale">Sale</option>
              </select>
            </div>
  
            <div class="form-group">
              <label for="location">Location</label>
              <input type="text" id="location" v-model="newProperty.location" required />
            </div>
  
            <div class="form-group">
              <label for="rooms">Rooms</label>
              <input type="number" id="rooms" v-model="newProperty.rooms" required />
            </div>
  
            <div class="form-group">
              <label for="area">Area (m²)</label>
              <input type="number" id="area" v-model="newProperty.area" required />
            </div>
  
            <div class="form-group">
              <label for="floor">Floor</label>
              <input type="number" id="floor" v-model="newProperty.floor" required />
            </div>
  
            <div class="form-group">
              <label for="amenities">Amenities (comma separated)</label>
              <input type="text" id="amenities" v-model="newProperty.amenities" />
            </div>
  
            <div class="form-group">
              <label for="price">Price</label>
              <input type="number" id="price" v-model="newProperty.price" required />
            </div>
  
            <div class="form-group">
              <label for="photos">Photos (comma separated URLs)</label>
              <input type="text" id="photos" v-model="newProperty.photos" />
            </div>
  
            <button type="submit" class="submit-button">Add Property</button>
          </form>
        </section>
      </main>
    </div>
  </template>
  
  <script>
  import HeaderLoader from "@/components/HeaderLoader.vue";
  import { API_BASE_URL } from "@/config/config.js";
  
  export default {
    name: "PropertySettingsPage",
    components: {
      HeaderLoader,
    },
    data() {
      return {
        currentPath: "/property-settings",
        newProperty: {
          description: '',
          propertyType: 'Apartment',
          transactionType: 'Rent',
          location: '',
          rooms: 0,
          area: 0,
          floor: 0,
          amenities: '',
          price: 0,
          photos: ''
        },
      };
    },
    methods: {
      async addProperty() {
        try {
          const propertyData = {
            description: this.newProperty.description,
            propertyType: this.newProperty.propertyType,
            transactionType: this.newProperty.transactionType,
            location: this.newProperty.location,
            rooms: this.newProperty.rooms,
            area: this.newProperty.area,
            floor: this.newProperty.floor,
            amenities: this.newProperty.amenities.split(',').map(amenity => amenity.trim()), 
            price: this.newProperty.price,
            photos: this.newProperty.photos.split(',').map(photo => photo.trim()), 
          };
  
          const response = await fetch(`${API_BASE_URL}/properties`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(propertyData),
          });
  
          if (!response.ok) {
            throw new Error('Failed to add property');
          }
  
          const newProperty = await response.json();
          
          this.$router.push({ name: 'propertyPage', params: { id: newProperty.id } });
        } catch (error) {
          console.error('Error adding property:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  @import url('../assets/css/styles.css');

  .container {
    max-width: 1200px;
    padding: 20px;
    margin: 0 auto;
    position: relative;
    top: 70px;
}

  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    font-weight: bold;
  }
  
  input,
  textarea,
  select {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  button.submit-button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    border: none;
    cursor: pointer;
  }
  
  button.submit-button:hover {
    background-color: #45a049;
  }
  </style>
  