'use client';

import React, { SVGProps } from 'react';

import { Icon } from '@iconify/react';
import { Button } from '@nextui-org/button';
import { Form } from '@nextui-org/form';
import { Input } from '@nextui-org/input';
import { useAuth } from '@/components/auth-provider';

export type IconSvgProps = SVGProps<SVGSVGElement> & {
  size?: number;
};

export default function Component() {
  const [isVisible, setIsVisible] = React.useState(false);
  const { login } = useAuth();

  const toggleVisibility = () => setIsVisible(!isVisible);

  const handleSubmit = (formdata: FormData) => {
    login(
      formdata.get('username') as string,
      formdata.get('password') as string,
    );
  };

  return (
    <div className="flex h-full w-full items-center justify-center">
      <div className="flex w-full max-w-sm flex-col gap-4 rounded-large">
        <div className="flex flex-col items-center pb-6">
          <p className="text-xl font-medium">С возвращением</p>
          <p className="text-small text-default-500">
            Войдите в свой аккаунт, чтобы продолжить
          </p>
        </div>
        <Form
          className="flex flex-col gap-3"
          validationBehavior="native"
          action={handleSubmit}>
          <Input
            isRequired
            label="Username"
            name="username"
            type="text"
            variant="bordered"
          />
          <Input
            isRequired
            endContent={
              <button type="button" onClick={toggleVisibility}>
                {isVisible ? (
                  <Icon
                    className="pointer-events-none text-2xl text-default-400"
                    icon="solar:eye-closed-linear"
                  />
                ) : (
                  <Icon
                    className="pointer-events-none text-2xl text-default-400"
                    icon="solar:eye-bold"
                  />
                )}
              </button>
            }
            label="Пароль"
            name="password"
            type={isVisible ? 'text' : 'password'}
            variant="bordered"
          />

          <Button className="w-full" color="primary" type="submit">
            Войти
          </Button>
        </Form>
      </div>
    </div>
  );
}
