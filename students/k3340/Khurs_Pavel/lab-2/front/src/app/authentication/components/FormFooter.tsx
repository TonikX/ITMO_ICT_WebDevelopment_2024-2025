import React from "react";
import { Button, Link } from "@nextui-org/react";

interface FormFooterProps {
  isLogin: boolean;
  onSwitch: () => void;
  pending: boolean;
  error?: string;
}

const FormFooter: React.FC<FormFooterProps> = ({
  isLogin,
  onSwitch,
  pending,
  error,
}) => {
  return (
    <div className="">
      <p className="text-center text-small">
        {isLogin ? (
          <>
            Создать аккаунт?{" "}
            <Link size="sm" onPress={onSwitch}>
              Регистрация
            </Link>
          </>
        ) : (
          <>
            У вас уже есть аккаунт?{" "}
            <Link size="sm" onPress={onSwitch}>
              Войти
            </Link>
          </>
        )}
      </p>
      <p className="text-red-400">{error}</p>
      <div className="flex gap-2 justify-end mt-4">
        <Button fullWidth color="primary" disabled={pending} type="submit">
          {isLogin ? "Войти" : "Зарегистрироваться"}
        </Button>
      </div>
    </div>
  );
};

export default FormFooter;
