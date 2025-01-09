import instance from './instance';
import { persist } from 'pinia-persists'
import RecipesApi from './recipes';

import { createPinia } from 'pinia'

const pinia = createPinia()


pinia.use(persist())


export default pinia

const recipesApi = new RecipesApi(instance);

export { recipesApi };
