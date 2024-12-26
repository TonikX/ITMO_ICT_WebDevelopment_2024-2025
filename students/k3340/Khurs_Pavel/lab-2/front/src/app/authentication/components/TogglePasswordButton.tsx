import React from "react";

import { EyeFilledIcon, EyeSlashFilledIcon } from "@/components/icons";

interface TogglePasswordButtonProps {
  isVisible: boolean;
  onClick: () => void;
}

const TogglePasswordButton: React.FC<TogglePasswordButtonProps> = ({
  isVisible,
  onClick,
}) => {
  return (
    <button
      aria-label="toggle password visibility"
      className="focus:outline-none"
      type="button"
      onClick={onClick}
    >
      {isVisible ? (
        <EyeSlashFilledIcon className="text-2xl text-default-400 pointer-events-none" />
      ) : (
        <EyeFilledIcon className="text-2xl text-default-400 pointer-events-none" />
      )}
    </button>
  );
};

export default TogglePasswordButton;
