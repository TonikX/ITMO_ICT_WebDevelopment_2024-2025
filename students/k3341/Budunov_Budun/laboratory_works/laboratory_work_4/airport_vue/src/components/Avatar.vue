<template>
    <div class="avatar-container" :style="{ width: size + 'px', height: size + 'px' }">
      <img
        v-if="imageUrl"
        :src="imageUrl"
        :alt="alt"
        class="avatar-image"
        :style="{ 'border-radius': radius }"
      />
      <div v-else class="default-avatar" :style="{ 'background-color': bgColor, 'border-radius': radius }">
        {{ initials }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  
  const props = defineProps({
    src: {
      type: String,
      required: false,
      default: '',
    },
    alt: {
      type: String,
      required: false,
      default: 'User Avatar',
    },
    size: {
      type: Number,
      required: false,
      default: 40,
    },
    fullName: {
      type: String,
      required: false,
      default: '',
    },
    bgColor: {
      type: String,
      required: false,
      default: '#007bff'
    },
    isCircle: {
      type: Boolean,
      required: false,
      default: true
    }
  });
  
  const imageUrl = computed(() => {
    if (props.src) {
      return props.src.startsWith('http') ? props.src : `http://localhost:8000${props.src}`;
    }
    return null;
  });
  
  const initials = computed(() => {
      if(props.fullName){
          const names = props.fullName.split(' ');
          return names.map(name => name.charAt(0).toUpperCase()).join('');
      }
      return "NA"
  })
  
  const radius = computed(() => {
    return props.isCircle ? '50%' : '10%';
  });
  </script>
  
  <style scoped>
  .avatar-container {
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }
  
  .avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .default-avatar {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      color: white;
  }
  </style>
  