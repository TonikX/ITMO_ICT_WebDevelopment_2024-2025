import { useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import {
  addDiet,
  deleteDiet,
  getDiets,
  updateDiet,
} from '../../features/diets/dietSlice'

import styles from './diets.module.css'

type DietData = {
  num: string
  name: string
  type: string
}

const DietsPage = () => {
  const [newDietData, setNewDietData] = useState<DietData>({
    num: '',
    name: '',
    type: '',
  })
  const [selectedDiet, setSelectedDiet] = useState<DietData | null>(null)
  const { diets, isLoading, isError, message } = useSelector(
    (state: any) => state.diets
  )
  const dispatch = useDispatch()
  const { user } = useSelector((state) => state.auth)

  useEffect(() => {
    if (user && user.access) {
      dispatch(getDiets(user.access))
    }
  }, [dispatch, user])

  const handleAddDiet = () => {
    if (user && user.access) {
      dispatch(addDiet({ data: newDietData, token: user.access }))
    }
    setNewDietData({ num: '', name: '', type: '' })
  }

  const handleEditClick = (diet: DietData) => {
    setSelectedDiet(diet)
    setNewDietData(diet)
  }

  const handleUpdateDiet = () => {
    if (selectedDiet && user && user.access) {
      dispatch(
        updateDiet({
          id: selectedDiet.id,
          data: newDietData,
          token: user.access,
        })
      )

      setSelectedDiet(null)
    }
  }

  const handleDeleteDiet = (id: string) => {
    if (user && user.access) {
      dispatch(deleteDiet({ id: id, token: user.access }))
    }
  }

  if (isLoading) return <p>Loading diets...</p>
  if (isError) return <p>Error: {message}</p>

  if (!Array.isArray(diets)) return <p>Error: Diets data is not an array</p>

  return (
    <div className={styles['container']}>
      <h1>Diets</h1>
      {diets.map((diet: DietData) => (
        <div key={diet.id} className={styles['diet_data_container']}>
          <h2>{diet.name}</h2>
          <p>Number: {diet.num}</p>
          {/* More details... */}
          <div className={styles['diet_btn--row']}>
            <button
              className={styles['diet_btn']}
              onClick={() => handleEditClick(diet)}
            >
              Edit
            </button>
            <button
              className={styles['diet_btn']}
              onClick={() => handleDeleteDiet(diet.id)}
            >
              Delete
            </button>
          </div>
        </div>
      ))}
      <div className={styles['diet_btn--column']}>
        {selectedDiet ? <h2>Edit Diet</h2> : <h2>Add New Diet</h2>}

        <input
            type='text'
            className={styles['diet_input']}
            placeholder='Number'
            value={newDietData.num}
            onChange={(e) =>
                setNewDietData({...newDietData, num: e.target.value})
            }
        />
        <input
            type='text'
            className={styles['diet_input']}
            placeholder='Name'
            value={newDietData.name}
            onChange={(e) =>
                setNewDietData({...newDietData, name: e.target.value})
            }
        />
        <input
            type='text'
            className={styles['diet_input']}
            placeholder='Type'
            value={newDietData.type}
            onChange={(e) =>
                setNewDietData({...newDietData, type: e.target.value})
            }
        />

        {selectedDiet ? (
            <button className={styles['diet_btn']} onClick={handleUpdateDiet}>
              Update Diet
            </button>
        ) : (
            <button className={styles['diet_btn']} onClick={handleAddDiet}>
              Add Diet
            </button>
        )}
      </div>
    </div>
  )
}

export default DietsPage
