import { ToggleButton } from 'react-bootstrap';

export const Switch = ({
  title,
  value,
  checked,
  setChecked,
}: {
  title: string;
  value: string;
  checked: boolean;
  setChecked: (checked: boolean) => void;
}) => {
  return (
    <ToggleButton
      className="mb-2"
      id="toggle-check"
      type="checkbox"
      variant="outline-primary"
      checked={checked}
      value={value}
      onChange={(e) => setChecked(e.currentTarget.checked)}
    >
      {title}
    </ToggleButton>
  );
};
