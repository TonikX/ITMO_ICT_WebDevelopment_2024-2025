import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import dietService from './dietService'

const initialState = {
  diets: [],
  isError: false,
  isSuccess: false,
  isLoading: false,
  message: '',
}

export const getDiets = createAsyncThunk(
  'diets/getAll',
  async (token, thunkAPI) => {
    try {
      return await dietService.getDiets(token)
    } catch (error) {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString()

      return thunkAPI.rejectWithValue(message)
    }
  }
)

export const addDiet = createAsyncThunk(
  'diets/add',
  async ({ data, token }, thunkAPI) => {
    try {
      return await dietService.addDiet(data, token)
    } catch (error) {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString()

      return thunkAPI.rejectWithValue(message)
    }
  }
)

export const updateDiet = createAsyncThunk(
  'diets/update',
  async ({ id, data, token }, thunkAPI) => {
    try {
      return await dietService.updateDiet(id, data, token)
    } catch (error) {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString()

      return thunkAPI.rejectWithValue(message)
    }
  }
)

export const deleteDiet = createAsyncThunk(
  'diets/delete',
  async ({ id, token }, thunkAPI) => {
    try {
      return await dietService.deleteDiet(id, token)
    } catch (error) {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString()

      return thunkAPI.rejectWithValue(message)
    }
  }
)

const dietSlice = createSlice({
  name: 'diet',
  initialState,
  reducers: {
    reset: (state) => initialState,
  },
  extraReducers: (builder) => {
    builder
      .addCase(getDiets.pending, (state) => {
        state.isLoading = true
      })
      .addCase(getDiets.fulfilled, (state, action) => {
        state.isLoading = false
        state.isSuccess = true
        state.diets = action.payload
      })
      .addCase(getDiets.rejected, (state, action) => {
        state.isLoading = false
        state.isError = true
        state.message = action.payload
      })
      .addCase(addDiet.pending, (state) => {
        state.isLoading = true
      })
      .addCase(addDiet.fulfilled, (state, action) => {
        state.isLoading = false
        state.isSuccess = true
        state.diets.push(action.payload)
      })
      .addCase(addDiet.rejected, (state, action) => {
        state.isLoading = false
        state.isError = true
        state.message = action.payload
      })
      .addCase(updateDiet.pending, (state) => {
        state.isLoading = true
      })
      .addCase(updateDiet.fulfilled, (state, action) => {
        state.isLoading = false
        state.isSuccess = true
        state.diets = state.diets.map((diet) =>
          diet.id === action.payload.id ? action.payload : diet
        )
      })
      .addCase(updateDiet.rejected, (state, action) => {
        state.isLoading = false
        state.isError = true
        state.message = action.payload
      })
      .addCase(deleteDiet.pending, (state) => {
        state.isLoading = true
      })
      .addCase(deleteDiet.fulfilled, (state, action) => {
        state.isLoading = false
        state.isSuccess = true
        state.diets = state.diets.filter(
          (diet) => diet.id !== action.payload
        )
      })
      .addCase(deleteDiet.rejected, (state, action) => {
        state.isLoading = false
        state.isError = true
        state.message = action.payload
      })
  },
})

export const { reset } = dietSlice.actions
export default dietSlice.reducer
