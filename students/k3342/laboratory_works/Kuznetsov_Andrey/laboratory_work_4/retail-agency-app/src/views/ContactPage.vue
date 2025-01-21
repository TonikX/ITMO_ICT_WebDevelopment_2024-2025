<template>
  <div>
    <HeaderLoader :currentPath="currentPath" />

    <main role="main" class="content">
      <div class="content-icon-container">
        <svg class="content-icon">
          <use xlink:href="#contactIcon"></use>
        </svg>
      </div>

      <div class="title">
        <h1>Get in Touch with Us</h1>
        <p>We're here to help with any questions or inquiries you have.</p>
      </div>

      <section class="details">
        <p>
          <strong>Phone:</strong> +1 (555) 123-4567<br />
          <strong>Email:</strong> support@rentease.com<br />
          <strong>Address:</strong> Saint-Josse-ten-Noode, Belgium 42, 1210
        </p>
      </section>

      <div class="map">
        <iframe
          id="gmap_canvas"
          src="https://maps.google.com/maps?q=50.854849,%204.373699&t=&z=13&ie=UTF8&output=embed"
          frameborder="0"
          scrolling="no"
          marginheight="0"
          marginwidth="0"
        ></iframe>
      </div>

      <section class="notes">
        <p>
          Feel free to reach out to us anytime during our business hours: Monday to Friday, 9:00 AM to 6:00 PM.
          Our support team will respond promptly to your queries and assist you with any needs.
        </p>
      </section>
    </main>
  </div>
</template>

<script>
import HeaderLoader from "@/components/HeaderLoader.vue";

export default {
  name: "ContactPage",
  components: {
    HeaderLoader,
  },
  data() {
    return {
      currentPath: "/contact",
    };
  },
};
</script>

<style scoped>
@import '../assets/css/styles.css';

.content .map iframe {
    display: block;
    margin: 0 auto; 
    border-radius: 5%; 
    width: 80%; 
    height: 500px; 
    border: none; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
    margin-bottom: 15px;
}
</style>