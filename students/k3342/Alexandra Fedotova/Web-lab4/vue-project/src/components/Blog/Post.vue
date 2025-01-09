<template>
  <div class="post-container">
    <!-- Кнопка возврата на блог -->
    <div class="back-btn-container">
      <router-link to="/blog" class="btn btn-primary">
        Back to Blog Search
      </router-link>
    </div>

    <div class="post-card">
      <h1 class="post-title">{{ post.title }}</h1>

      <img :src="post.image" alt="Post Image" class="post-image" />

      <div class="post-content" v-html="formattedContent"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Post',
  data() {
    return {
      post: {
        title: 'The Benefits of Staying Hydrated',
        image: '/public/hydro.jpg',
        content: `
          <p>Staying hydrated is crucial for maintaining optimal health and well-being. Water is essential for various bodily functions, from regulating body temperature to supporting metabolism and nutrient absorption. Despite its importance, many people overlook the need for proper hydration. In this article, we will explore the numerous benefits of staying hydrated and why it's essential to drink enough water each day.</p>

          <h2>1. Maintains Fluid Balance</h2>
          <p>Water plays a key role in maintaining fluid balance within the body. It helps transport nutrients to cells, remove waste products, and regulate body temperature. The human body is composed of approximately 60% water, and this fluid is constantly being lost through sweat, urine, and respiration. Therefore, it’s essential to replenish water intake throughout the day to maintain proper fluid balance.</p>

          <h2>2. Supports Digestion</h2>
          <p>Proper hydration aids in the digestion process by facilitating the movement of food through the gastrointestinal tract. It helps break down food particles and enables the absorption of nutrients in the stomach and intestines. Without adequate water, your digestive system can become sluggish, leading to problems such as constipation and indigestion.</p>

          <h2>3. Boosts Energy Levels</h2>
          <p>Dehydration can cause fatigue, lethargy, and a decrease in cognitive function. Drinking enough water helps maintain energy levels by preventing the body from becoming sluggish. It also supports the brain’s function, improving concentration and memory, making you more productive throughout the day.</p>

          <h2>4. Enhances Skin Health</h2>
          <p>Staying hydrated is essential for healthy, glowing skin. Water helps flush out toxins and keeps skin cells nourished. Dehydration can lead to dry, flaky skin, as well as an increased risk of wrinkles and other skin issues. Drinking enough water helps maintain skin elasticity and can promote a healthy complexion.</p>

          <h2>5. Regulates Body Temperature</h2>
          <p>One of the most important functions of water is temperature regulation. Water helps to cool the body through sweating and evaporation, preventing overheating. This is particularly important during exercise or hot weather when the body is more prone to dehydration.</p>

          <h2>6. Improves Physical Performance</h2>
          <p>When exercising, staying hydrated is essential to maintain physical performance. Water helps regulate muscle function, improve endurance, and prevent cramps. Dehydration can lead to decreased strength, coordination, and stamina, making it difficult to achieve your fitness goals.</p>

          <h2>7. Promotes Kidney Health</h2>
          <p>The kidneys play a vital role in filtering toxins from the blood and producing urine. Adequate hydration ensures that the kidneys can function properly, reducing the risk of kidney stones and urinary tract infections (UTIs). Dehydration can cause kidney damage over time, as the kidneys must work harder to filter waste products without enough fluid.</p>

          <p><strong>Conclusion:</strong></p>
          <p>Hydration is key to overall health and well-being. From supporting bodily functions to improving skin health, digestion, and mental clarity, the benefits of drinking enough water are vast. Aim to drink at least 8 cups (about 2 liters) of water daily, or more if you are active or live in a hot climate. Your body will thank you for it, and you'll feel better, both physically and mentally, as a result. So, drink up and stay hydrated!</p>
        `
      },
    };
  },
  computed: {
    formattedContent() {
      return this.post.content;
    }
  }
};
</script>

<style scoped>
:root {
  --background-color: #fbeaff;
  --text-color: #333;
  --card-background: #fff;
  --heading-color: #6a0dad;
  --button-background: #ff85c0;
  --button-border: #ff85c0;
}

.post-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.back-btn-container {
  margin-bottom: 20px;
}

.post-card {
  background-color: var(--card-background);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 20px;
  max-width: 1000px;
  margin: 20px 0;
  text-align: center;
  font-family: Arial, sans-serif;
}

.post-title {
  color: var(--heading-color);
  font-size: 2rem;
  margin-bottom: 15px;
  font-weight: bold;
}
.post-image {
  width: 100%;
  height: 600px;
  object-fit: cover;
  margin-bottom: 20px;
  border-radius: 8px;
}

.post-content {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--text-color);
  padding: 0 10px;
  text-align: justify;
  margin-top: 20px;
}
.post-content h2 {
  color: var(--heading-color);
  font-size: 1.5rem;
  margin-top: 15px;
  font-weight: bold;
}

h2 {
  color: var(--heading-color);
  font-size: 1.5rem;
  margin-top: 15px;
  font-weight: bold;
}

p {
  margin-bottom: 15px;
}

.btn-primary {
  background-color: var(--button-background);
  border-color: var(--button-border);
  color: var(--text-color);
  padding: 10px 20px;
  text-align: center;
  font-size: 1.1rem;
  display: inline-block;
  margin: 20px 0;
  text-decoration: none;
}

.btn-primary:hover {
  background-color: var(--button-border);
}

@media (max-width: 768px) {
  .post-title {
    font-size: 1.8rem;
  }

  .post-content {
    font-size: 1rem;
  }
}
</style>
