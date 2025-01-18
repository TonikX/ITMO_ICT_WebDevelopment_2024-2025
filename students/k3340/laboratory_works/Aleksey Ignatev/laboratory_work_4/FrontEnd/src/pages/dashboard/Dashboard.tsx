import { useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import {
    getAnimalsIn,
} from '../../features/animals/animalSlice'

import styles from '../animals/animals.module.css'

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

type CageData = {
    name: string
    count_animals_in: number,
    animals_in: AnimalData[]
}

const Dashboard = () => {
    const { animalsIn, isLoading, isError, message } = useSelector(
        (state: any) => state.animals
    )

    const dispatch = useDispatch()
    const { user } = useSelector((state) => state.auth)

    useEffect(() => {
        if (user && user.access) {
            dispatch(getAnimalsIn(user.access))
        }
    }, [dispatch, user])

    if (isLoading) return <p>Loading animals...</p>
    if (isError) return <p>Error: {message}</p>

    if (!Array.isArray(animalsIn)) return <p>Error: Animals data is not an array</p>

    return (
        <div className={styles['container']}>
            <h1>Animals In cages</h1>
            {animalsIn.map((cage: CageData) => (
                <div className={styles['animal_data_container']}>
                    <h2>Cage: {cage.name}</h2>
                    <p>Animals IN: {cage.count_animals_in}</p>
                    {/* More details... */}
                    {cage.animals_in.map((animal: AnimalData) => (
                        <div key={animal.id} className={styles['animal_data_container']}>
                            <h2>{animal.name}</h2>
                            <p>Number: {animal.num}</p>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    )
}

export default Dashboard
