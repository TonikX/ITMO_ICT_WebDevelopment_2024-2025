import { configureStore } from '@reduxjs/toolkit'
import authReducer from '../features/auth/authSlice'
import animalReducer from '../features/animals/animalSlice'
import dietReducer from '../features/diets/dietSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    animals: animalReducer,
    diets: dietReducer,
  },
})
