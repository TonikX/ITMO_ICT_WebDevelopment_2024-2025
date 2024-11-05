"use client";
import { useAuth } from "@/context/AuthContext";

import { Button } from "@nextui-org/button";
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
} from "@nextui-org/react";
import { useRouter } from "next/navigation";

interface UserDropdownProps {
  email?: string;
}
const UserDropdown = ({ email }: UserDropdownProps) => {
  const { logout } = useAuth();
  const router = useRouter();
  const dropdownAction = async () => {
    const res = await logout();

    if (res?.status === 201) {
      router.replace("/authentication");
    }
  };

  return (
    <Dropdown>
      <DropdownTrigger>
        <Button variant="light">{email}</Button>
      </DropdownTrigger>
      <DropdownMenu aria-label="Action event example" onAction={dropdownAction}>
        <DropdownItem key="delete" className="text-danger" color="danger">
          Выйти
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
};

export default UserDropdown;
