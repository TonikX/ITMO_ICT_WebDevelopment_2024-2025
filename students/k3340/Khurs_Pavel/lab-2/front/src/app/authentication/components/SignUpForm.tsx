"use client";

import React, { FC, useState } from "react";
import { Input } from "@nextui-org/react";
import { useFormStatus } from "react-dom";

import TogglePasswordButton from "./TogglePasswordButton";

import FormFooter from "@/app/authentication/components/FormFooter";
import { useAuth } from "@/context/AuthContext";

interface SignUpFormProps {
  onSwitch: () => void; // Функция для переключения на Login
}

const SignUpForm: FC<SignUpFormProps> = ({ onSwitch }) => {
  const [isVisible, setIsVisible] = useState(false);
  const { register } = useAuth();
  const [formMessage, setFromMessage] = useState("");

  const signUp = async (formData: FormData) => {
    const res = await register(
      formData.get("name") as string,
      formData.get("email") as string,
      formData.get("password") as string
    );

    if (res.message) {
      setFromMessage(res.message);
    }
  };
  const { pending } = useFormStatus();

  return (
    <form
      action={signUp}
      className="flex flex-col justify-between gap-4 h-full"
    >
      <div className="">
        <Input
          isRequired
          className="mt-4"
          label="Имя"
          name="name"
          placeholder="Введите ваше имя"
          type="text"
        />
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
          placeholder="Введите пароль"
          type={isVisible ? "text" : "password"}
        />
      </div>
      <FormFooter
        isLogin={false}
        error={formMessage}
        pending={pending}
        onSwitch={onSwitch}
      />
    </form>
  );
};

export default SignUpForm;
