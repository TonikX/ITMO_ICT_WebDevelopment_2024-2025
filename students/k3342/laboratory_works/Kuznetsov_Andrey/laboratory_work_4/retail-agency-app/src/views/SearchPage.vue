<template>
 <HeaderLoader :currentPath="currentPath" />

  <div>
    <div class="content">
      <h1 class="title">Real Estate Search</h1>
      <div class="row">

        <aside class="search-sidebar" aria-labelledby="searchTitle" role="complementary">
          <form id="searchForm" aria-describedby="searchTitle" @submit.prevent="handleSearch">

            <div class="form-group">
              <label for="propertyType" class="form-label">Property Type</label>
              <select v-model="filters.propertyType" id="propertyType" class="form-select">
                <option value="">All</option>
                <option value="apartment">Apartment</option>
                <option value="house">House</option>
                <option value="condo">Condominium</option>
                <option value="land">Land</option>
              </select>
            </div>

            <div class="form-group">
              <label for="purchaseRent" class="form-label">Transaction Type</label>
              <select v-model="filters.transactionType" id="purchaseRent" class="form-select">
                <option value="">All</option>
                <option value="rent">Rent</option>
                <option value="buy">Buy</option>
                <option value="lease">Lease</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Number of Rooms</label>
              <div class="checkbox-group">
                <div v-for="n in [0, 1, 2, 3, 4]" :key="'room' + n">
                  <input
                    type="checkbox"
                    :id="'room' + n"
                    :value="n"
                    v-model="filters.rooms"
                  />
                  <label :for="'room' + n">{{ n === 0 ? 'Studio' : n }}</label>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Amenities</label>
              <div class="checkbox-group">
                <div v-for="amenity in ['pool', 'gym', 'garage', 'garden']" :key="'amenity' + amenity">
                  <input
                    type="checkbox"
                    :id="'amenity' + amenity"
                    :value="amenity"
                    v-model="filters.amenities"
                  />
                  <label :for="'amenity' + amenity">{{ amenity.charAt(0).toUpperCase() + amenity.slice(1) }}</label>
                </div>
              </div>
            </div>
            
            <div class="form-group range-container">
              <label class="form-label">Area Range</label>
              <div class="range">
                <input
                  type="text"
                  id="minArea"
                  v-model="filters.minArea"
                  placeholder="Min"
                  class="form-control mt-2"
                  readonly
                />
                <input
                  type="text"
                  id="maxArea"
                  v-model="filters.maxArea"
                  placeholder="Max"
                  class="form-control mt-2"
                  readonly
                />
              </div>
            </div>


            <div class="form-group range-container">
              <label class="form-label">Price Range</label>
              <div class="range">
                <input
                  type="text"
                  id="minPrice"
                  v-model="filters.minPrice"
                  placeholder="Min"
                  class="form-control mt-2"
                  readonly
                />
                <input
                  type="text"
                  id="maxPrice"
                  v-model="filters.maxPrice"
                  placeholder="Max"
                  class="form-control mt-2"
                  readonly
                />
              </div>
            </div>

             <div class="form-group">
              <label for="location" class="form-label">Location</label>
                <input
                    type="text"
                    id="location"
                    v-model="filters.location"
                    class="form-control"
                    placeholder="Enter city or area"
                />
            </div>
            

            <div class="form-group">
              <label for="sortBy" class="form-label">Sort By</label>
              <select v-model="filters.sortBy" id="sortBy" class="form-select">
                <option value="default">Default</option>
                <option value="priceAsc">Price (Low to High)</option>
                <option value="priceDesc">Price (High to Low)</option>
                <option value="roomsAsc">Rooms (Low to High)</option>
                <option value="roomsDesc">Rooms (High to Low)</option>
                <option value="newest">Newest Listings</option>
              </select>
            </div>

            <button type="submit" class="btn btn-primary">Search</button>
          </form>
        </aside>

        <main class="col-md-9 results-container" role="main">
          <div v-if="loading" class="mt-5">Loading...</div>
          <div v-else-if="properties.length === 0" class="mt-5"></div>
          <div v-else id="searchResults" class="mt-5" aria-live="polite">
            <div v-for="property in properties" :key="property.id" class="property-item">
              <div class="property-image">
                <img :src="property.photos[0]" :alt="property.propertyType" />
              </div>
              <div class="property-details">
                <h3>{{ property.propertyType }} - {{ property.transactionType }}</h3>
                <p>Location: {{ property.location }}</p>
                <p>Rooms: {{ property.rooms }} | Area: {{ property.area }} m²</p>
                <p>Price: ${{ property.price.toLocaleString() }}</p>
                <button @click="viewPropertyDetails(property.id)" class="view-details">View Details</button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderLoader from "@/components/HeaderLoader.vue";
import { API_BASE_URL } from "@/config/config.js";

export default {
  name: "SearchPage",
  components: {
     HeaderLoader,
  },
  data() {
    return {
      currentPath: "/search",
      filters: {
        propertyType: "",
        transactionType: "",
        rooms: [],
        amenities: [],
        location: "",
        minPrice: "",
        maxPrice: "",
        minArea: "",
        maxArea: "",
        sortBy: "default",
      },
      properties: [],
      loading: false,
    };
  },
  methods: {
    async handleSearch() {
      this.loading = true;
      const filters = { ...this.filters };

      try {
        const queryParams = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE_URL}/properties?${queryParams}`);
        const properties = await response.json();
        this.properties = properties;
      } catch (error) {
        console.error("Error fetching properties:", error);
      } finally {
        this.loading = false;
      }
    },
    viewPropertyDetails(propertyId) {
      this.$router.push({ name: 'Property', params: { id: propertyId } });
    },
  },
};
</script>

<style scoped>
@import url('../assets/css/search.css');
@import url('../assets/css/styles.css');
</style>