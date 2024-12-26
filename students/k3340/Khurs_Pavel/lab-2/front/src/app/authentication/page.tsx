"use client";
import React, { useState } from "react";
import { Tabs, Tab, Card, CardBody } from "@nextui-org/react";

import LoginForm from "@/app/authentication/components/LoginForm";
import SignUpForm from "@/app/authentication/components/SignUpForm";

export default function App() {
  const [selected, setSelected] = useState<string | number>("login");

  const handleSwitch = () => {
    setSelected(selected === "login" ? "sign-up" : "login");
  };

  return (
    <div className="flex flex-col items-center min-w-full">
      <Card fullWidth className="sm:max-w-[30%]">
        <CardBody className="overflow-hidden">
          <Tabs
            fullWidth
            aria-label="Tabs form"
            selectedKey={selected}
            size="md"
            onSelectionChange={(key) => setSelected(key)}
          >
            <Tab key="login" className="h-full" title="Вход">
              <LoginForm onSwitch={handleSwitch} />
            </Tab>
            <Tab key="sign-up" className="h-full" title="Регистрация">
              <SignUpForm onSwitch={handleSwitch} />
            </Tab>
          </Tabs>
        </CardBody>
      </Card>
    </div>
  );
}
