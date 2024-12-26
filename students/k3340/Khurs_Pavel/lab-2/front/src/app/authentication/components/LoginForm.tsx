"use client";

import React, { FC, useState } from "react";
import { Input } from "@nextui-org/react";
import { useFormStatus } from "react-dom";

import TogglePasswordButton from "./TogglePasswordButton";

import FormFooter from "@/app/authentication/components/FormFooter";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

interface LoginFormProps {
  onSwitch: () => void; // Функция для переключения на SignUp
}

const LoginForm: FC<LoginFormProps> = ({ onSwitch }) => {
  const [isVisible, setIsVisible] = useState(false);
  const [formMessage, setFromMessage] = useState("");
  const { login } = useAuth();
  const { pending } = useFormStatus();
  const route = useRouter();
  const formAction = async (formData: FormData) => {
    const res = await login(
      formData.get("email") as string,
      formData.get("password") as string
    );

    if (res.message) {
      setFromMessage(res.message);
    }
    route.replace("/");
  };

  return (
    <form
      action={formAction}
      className="flex flex-col gap-y-4 justify-between h-full"
    >
      <div>
        <Input
          isRequired
          className="mt-4"
          label="Email"
          name="email"
          placeholder="Введите email"
          type="email"
        />
        <Input
          isRequired
          className="mt-4"
          endContent={
            <TogglePasswordButton
              isVisible={isVisible}
              onClick={() => setIsVisible(!isVisible)}
            />
          }
          label="Пароль"
          name="password"
          placeholder="Ведите пароль"
          type={isVisible ? "text" : "password"}
        />
      </div>
      <FormFooter
        isLogin
        error={formMessage}
        pending={pending}
        onSwitch={onSwitch}
      />
    </form>
  );
};

export default LoginForm;
