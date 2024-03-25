'use client'

import Button from '@/components/buttons'
import axios from 'axios'
import React from 'react'
import { useForm } from 'react-hook-form'
import { useRouter } from 'next/navigation';
import { loginUser } from '@/components/Auth'

const Login = () => {
    const { register, handleSubmit, formState: { errors }, setError } = useForm();

    const router = useRouter();
    
    const login = async(data) => {
        const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}login`, data)

        if (response.data.status === 'success') {
            const { id, username } = response.data.message;
            loginUser(id, username);
            router.replace('/')
        } else {
            setError('login', { type: 'custom', message: response.data.message });
        }
    }

    return (
        <section className='bg-white border-2 shadow-lg flex flex-col justify-around items-center h-[25rem] w-[20rem] rounded-lg'>
            <div>
                <h1>LOGIN</h1>
            </div>
            <div>
                <form onSubmit={handleSubmit(login)} className='flex flex-col gap-5 items-center'>
                    <div className='flex flex-col gap-1 items-center'>
                    <input
                        type="text"
                        placeholder="USERNAME"
                        className='border-b outline-none focus:border-blue-500'
                        {...register('username', { required: 'Username is required' })}
                    />
                    {errors.username && <span className='text-red-600'>{errors.username.message}</span>}
                    </div>
                    <div className='flex flex-col gap-1 items-center'>
                    <input
                        type="password"
                        placeholder="PASSWORD"
                        className='border-b outline-none focus:border-blue-500'
                        {...register('password', { required: 'Password is required' })}
                    />
                    {errors.password && <span className='text-red-600'>{errors.password.message}</span>}
                    </div>
                    <Button type="submit" value='Login' variant='primary' />
                    {errors.login && <span className='text-red-600'>{errors.login.message}</span>}
                </form>
            </div>
        </section>
    )
}

export default Login
