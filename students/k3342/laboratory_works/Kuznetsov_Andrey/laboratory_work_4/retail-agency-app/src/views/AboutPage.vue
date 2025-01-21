<template>
  <div>
    <HeaderLoader :currentPath="currentPath" />

    <main role="main" class="content">
      <div class="content-icon-container">
        <svg class="content-icon">
          <use xlink:href="#companyIcon"></use>
        </svg>
      </div>

      <div class="title">
        <h1>Welcome to Retail Agency!</h1>
        <p>Your trusted partner in renting and leasing properties with ease and reliability.</p>
      </div>

      <section class="description">
        <p>
          At RentEase, we simplify the process of renting properties. Whether you're a homeowner looking to lease
          out your property or a tenant searching for the perfect home, our platform is designed to make the
          experience seamless and stress-free. We believe in transparency, trust, and technology as the pillars of
          our service.
        </p>
        <p>
          Our story began with a simple mission: to revolutionize the way people approach rental properties. With
          cutting-edge tools, user-friendly interfaces, and a dedicated support team, RentEase has become a
          one-stop solution for all rental needs.
        </p>
      </section>

      <div class="image-container">
        <img src="../assets/images/about/cool-office.jpg" alt="A modern rental property" class="about-image">
      </div>

      <section class="details">
        <p>
          We specialize in providing an extensive range of rental options, from cozy apartments to luxurious
          villas. Our platform connects property owners with potential tenants in a secure and efficient manner.
          Advanced search filters, AI-driven recommendations, and personalized support ensure that every user finds
          exactly what they're looking for.
        </p>
        <p>
          With thousands of satisfied clients and years of experience in the industry, RentEase continues to set
          new standards in property rentals. Join our growing community and experience the future of real estate
          leasing today.
        </p>
      </section>
    </main>
  </div>
</template>

<script>
import HeaderLoader from "@/components/HeaderLoader.vue";

export default {
  name: "AboutPage",
  components: {
    HeaderLoader,
  },
  data() {
    return {
      currentPath: "/about",
    };
  },
};
</script>

<style scoped>
@import '../assets/css/styles.css';

.content img {
    display: block;
    margin: 0 auto;
    border-radius: 5%;
    width: 500px;
    height: 250px;
    object-fit: cover;
    object-position: center;
    margin-bottom: 30px;
}
</style>