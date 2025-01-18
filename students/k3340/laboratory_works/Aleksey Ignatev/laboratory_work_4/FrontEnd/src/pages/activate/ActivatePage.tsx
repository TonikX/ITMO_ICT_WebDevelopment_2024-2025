import { useEffect } from 'react'
import { BiUserCheck } from 'react-icons/bi'
import { useNavigate, useParams } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { toast } from 'react-toastify'
import Spinner from '../../components/Spinner'
import { activate, reset } from '../../features/auth/authSlice'

const ActivatePage = () => {
  const { uid, token } = useParams()
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const { isLoading, isError, isSuccess, message } = useSelector(
    (state) => state.auth
  )

  const handleSubmit = (e) => {
    e.preventDefault()

    const userData = {
      uid,
      token,
    }
    dispatch(activate(userData))
  }

  useEffect(() => {
    if (isError) {
      toast.error(message)
    }

    if (isSuccess) {
      navigate('/login')
      toast.success('Your account has been activated! You can login now')
    }

    dispatch(reset())
  }, [isError, isSuccess, navigate, dispatch])

  return (
    <div>
      <div className='container auth__container'>
        <h1 className='main__title'>
          Activate Account <BiUserCheck />{' '}
        </h1>

        {(isLoading && <Spinner />) || (
          <button
            className='btn btn-accent btn-activate-account'
            type='submit'
            onClick={handleSubmit}
          >
            Activate Account
          </button>
        )}
      </div>
    </div>
  )
}

export default ActivatePage
