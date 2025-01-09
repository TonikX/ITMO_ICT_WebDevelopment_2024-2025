import { ref } from 'vue';
import axios from 'axios';

const DEFAULT_IMAGE = '/src/assets/images/cooking.png';

export function useRecipes(url) {
  const recipes = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const groupRecipes = (recipes) => {
    const chunkSize = 3;
    return recipes.reduce((resultArray, item, index) => {
      const chunkIndex = Math.floor(index / chunkSize);
      if (!resultArray[chunkIndex]) {
        resultArray[chunkIndex] = [];
      }
      resultArray[chunkIndex].push(item);
      return resultArray;
    }, []);
  };

  const fetchRecipes = async () => {
  loading.value = true;
  try {
    const response = await axios.get(url);

    recipes.value = response.data.map(recipe => ({
      ...recipe,
      image: recipe.image ? recipe.image : DEFAULT_IMAGE,
      author_username: recipe.author?.username || 'Неизвестен',
    }));

    return groupRecipes(recipes.value);
  } catch (err) {
    error.value = 'Ошибка при загрузке рецептов';
    console.error(err);
  } finally {
    loading.value = false;
  }
};


  return { recipes, loading, error, fetchRecipes, groupRecipes };
}
