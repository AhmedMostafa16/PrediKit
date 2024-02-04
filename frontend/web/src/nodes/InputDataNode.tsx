import { CloseButton, Input, InputWrapper } from '@mantine/core';
import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';
import { useState } from 'react';

export interface InputDataNode extends BaseNode {
  data: InputDataNodeDataModel;
}

interface InputDataNodeDataModel extends PropertiesBase {
  file?: string;
  // TODO: uncomment whenever you decide to switch from passing
  // a file path to a BytesIO Object
  // extension?: string;
}

export default function InputDataNodePropertiesUI({ data }: { data: InputDataNodeDataModel }) {
  const [value, setValue] = useState<string>('');

  return (
    <>
      <InputWrapper label="File Path" required>
        <Input
          type="text"
          placeholder="Enter file path"
          value={value}
          onChange={(event) => {
            setValue(event.currentTarget.value);
            data.file = value;
          }}
          rightSectionPointerEvents="all"
          mt="md"
          rightSection={
            <CloseButton
              aria-label="Clear input"
              onClick={() => setValue('')}
              style={{ display: value ? undefined : 'none' }}
            />
          }
        />
      </InputWrapper>
    </>
  );
}
