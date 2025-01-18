import {createSlice, createAsyncThunk} from '@reduxjs/toolkit'
import animalService from './animalService'

const initialState = {
    animals: [],
    animalsIn: [],
    isError: false,
    isSuccess: false,
    isLoading: false,
    message: '',
}

export const getAnimals = createAsyncThunk(
    'animals/getAll',
    async (token, thunkAPI) => {
        try {
            return await animalService.getAnimals(token)
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

export const getAnimalsIn = createAsyncThunk(
    'animals/getAllIn',
    async (token, thunkAPI) => {
        try {
            return await animalService.getAnimalsIn(token)
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

export const addAnimal = createAsyncThunk(
    'animals/add',
    async ({data, token}, thunkAPI) => {
        try {
            return await animalService.addAnimal(data, token)
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

export const updateAnimal = createAsyncThunk(
    'animals/update',
    async ({id, data, token}, thunkAPI) => {
        try {
            return await animalService.updateAnimal(id, data, token)
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

export const deleteAnimal = createAsyncThunk(
    'animals/delete',
    async ({id, token}, thunkAPI) => {
        try {
            return await animalService.deleteAnimal(id, token)
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

const animalSlice = createSlice({
    name: 'animal',
    initialState,
    reducers: {
        reset: (state) => initialState,
    },
    extraReducers: (builder) => {
        builder
            .addCase(getAnimals.pending, (state) => {
                state.isLoading = true
            })
            .addCase(getAnimals.fulfilled, (state, action) => {
                state.isLoading = false
                state.isSuccess = true
                state.animals = action.payload
            })
            .addCase(getAnimals.rejected, (state, action) => {
                state.isLoading = false
                state.isError = true
                state.message = action.payload
            })
            .addCase(getAnimalsIn.pending, (state) => {
                state.isLoading = true
            })
            .addCase(getAnimalsIn.fulfilled, (state, action) => {
                state.isLoading = false
                state.isSuccess = true
                state.animalsIn = action.payload
            })
            .addCase(getAnimalsIn.rejected, (state, action) => {
                state.isLoading = false
                state.isError = true
                state.message = action.payload
            })
            .addCase(addAnimal.pending, (state) => {
                state.isLoading = true
            })
            .addCase(addAnimal.fulfilled, (state, action) => {
                state.isLoading = false
                state.isSuccess = true
                state.animals.push(action.payload)
            })
            .addCase(addAnimal.rejected, (state, action) => {
                state.isLoading = false
                state.isError = true
                state.message = action.payload
            })
            .addCase(updateAnimal.pending, (state) => {
                state.isLoading = true
            })
            .addCase(updateAnimal.fulfilled, (state, action) => {
                state.isLoading = false
                state.isSuccess = true
                state.animals = state.animals.map((animal) =>
                    animal.id === action.payload.id ? action.payload : animal
                )
            })
            .addCase(updateAnimal.rejected, (state, action) => {
                state.isLoading = false
                state.isError = true
                state.message = action.payload
            })
            .addCase(deleteAnimal.pending, (state) => {
                state.isLoading = true
            })
            .addCase(deleteAnimal.fulfilled, (state, action) => {
                state.isLoading = false
                state.isSuccess = true
                state.animals = state.animals.filter(
                    (animal) => animal.id !== action.payload
                )
            })
            .addCase(deleteAnimal.rejected, (state, action) => {
                state.isLoading = false
                state.isError = true
                state.message = action.payload
            })
    },
})

export const {reset} = animalSlice.actions
export default animalSlice.reducer
