import { useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import {
  addAnimal,
  deleteAnimal,
  getAnimals,
  updateAnimal,
} from '../../features/animals/animalSlice'

import styles from './animals.module.css'

type AnimalData = {
  num: string
  name: string
  age: number
  sex: 'm' | 'f'
  diet: string
  birthdate: string
  owner: string
  previous_owner: string
  in_lease: boolean
  where_is_now: string
  since: string
}

const AnimalsPage = () => {
  const [newAnimalData, setNewAnimalData] = useState<AnimalData>({
    num: '',
    name: '',
    age: 0,
    sex: 'm',
    diet: '',
    birthdate: '', // Add a state for birthdate
    owner: '', // Add a state for owner
    previous_owner: '', // Add a state for previous owner
    in_lease: false, // Add a state for in_lease
    where_is_now: '', // Add a state for where_is_now
    since: '', // Add a state for since
  })
  const [selectedAnimal, setSelectedAnimal] = useState<AnimalData | null>(null)
  const { animals, isLoading, isError, message } = useSelector(
    (state: any) => state.animals
  )
  const dispatch = useDispatch()
  const { user } = useSelector((state) => state.auth)

  useEffect(() => {
    if (user && user.access) {
      dispatch(getAnimals(user.access))
    }
  }, [dispatch, user])

  const handleAddAnimal = () => {
    if (user && user.access) {
      dispatch(addAnimal({ data: newAnimalData, token: user.access }))
    }
    setNewAnimalData({ num: '', name: '', age: 0, sex: 'm', diet: '' })
  }

  const handleEditClick = (animal: AnimalData) => {
    setSelectedAnimal(animal)
    setNewAnimalData(animal)
  }

  const handleUpdateAnimal = () => {
    if (selectedAnimal && user && user.access) {
      dispatch(
        updateAnimal({
          id: selectedAnimal.id,
          data: newAnimalData,
          token: user.access,
        })
      )

      setSelectedAnimal(null)
    }
  }

  const handleDeleteAnimal = (id: string) => {
    if (user && user.access) {
      dispatch(deleteAnimal({ id: id, token: user.access }))
    }
  }

  if (isLoading) return <p>Loading animals...</p>
  if (isError) return <p>Error: {message}</p>

  if (!Array.isArray(animals)) return <p>Error: Animals data is not an array</p>

  return (
    <div className={styles['container']}>
      <h1>Animals</h1>
      {animals.map((animal: AnimalData) => (
        <div key={animal.id} className={styles['animal_data_container']}>
          <h2>{animal.name}</h2>
          <p>Number: {animal.num}</p>
          {/* More details... */}
          <div className={styles['animal_btn--row']}>
            <button
              className={styles['animal_btn']}
              onClick={() => handleEditClick(animal)}
            >
              Edit
            </button>
            <button
              className={styles['animal_btn']}
              onClick={() => handleDeleteAnimal(animal.id)}
            >
              Delete
            </button>
          </div>
        </div>
      ))}
      <div className={styles['animal_btn--column']}>
        {selectedAnimal ? <h2>Edit Animal</h2> : <h2>Add New Animal</h2>}

        <input
          type='text'
          className={styles['animal_input']}
          placeholder='Number'
          value={newAnimalData.num}
          onChange={(e) =>
            setNewAnimalData({ ...newAnimalData, num: e.target.value })
          }
        />
        <input
          type='text'
          className={styles['animal_input']}
          placeholder='Name'
          value={newAnimalData.name}
          onChange={(e) =>
            setNewAnimalData({ ...newAnimalData, name: e.target.value })
          }
        />
        <input
          type='number'
          className={styles['animal_input']}
          placeholder='Age'
          value={newAnimalData.age}
          onChange={(e) =>
            setNewAnimalData({ ...newAnimalData, age: Number(e.target.value) })
          }
        />
        <select
          value={newAnimalData.sex}
          className={styles['animal_input']}
          onChange={(e) =>
            setNewAnimalData({
              ...newAnimalData,
              sex: e.target.value as 'm' | 'f',
            })
          }
        >
          <option value='m'>Male</option>
          <option value='f'>Female</option>
        </select>
        <input
          type='text'
          className={styles['animal_input']}
          placeholder='Diet'
          value={newAnimalData.diet}
          onChange={(e) =>
            setNewAnimalData({ ...newAnimalData, diet: e.target.value })
          }
        />
        <input
          type='date'
          className={styles['animal_input']}
          placeholder='Birthdate'
          value={newAnimalData.birthdate}
          onChange={(e) =>
            setNewAnimalData({ ...newAnimalData, birthdate: e.target.value })
          }
        />
        <input
          type='text'
          className={styles['animal_input']}
          placeholder='Owner'
          value={newAnimalData.owner}
          onChange={(e) =>
            setNewAnimalData({ ...newAnimalData, owner: e.target.value })
          }
        />
        <input
          type='text'
          className={styles['animal_input']}
          placeholder='Previous Owner'
          value={newAnimalData.previous_owner}
          onChange={(e) =>
            setNewAnimalData({
              ...newAnimalData,
              previous_owner: e.target.value,
            })
          }
        />
        <label>
          In Lease:
          <input
            type='checkbox'
            className={styles['animal_input']}
            checked={newAnimalData.in_lease}
            onChange={(e) =>
              setNewAnimalData({ ...newAnimalData, in_lease: e.target.checked })
            }
          />
        </label>
        <input
          type='text'
          className={styles['animal_input']}
          placeholder='Where is now'
          value={newAnimalData.where_is_now}
          onChange={(e) =>
            setNewAnimalData({ ...newAnimalData, where_is_now: e.target.value })
          }
        />
        <input
          type='date'
          className={styles['animal_input']}
          placeholder='Since'
          value={newAnimalData.since}
          onChange={(e) =>
            setNewAnimalData({ ...newAnimalData, since: e.target.value })
          }
        />

        {selectedAnimal ? (
          <button className={styles['animal_btn']} onClick={handleUpdateAnimal}>
            Update Animal
          </button>
        ) : (
          <button className={styles['animal_btn']} onClick={handleAddAnimal}>
            Add Animal
          </button>
        )}
      </div>
    </div>
  )
}

export default AnimalsPage
