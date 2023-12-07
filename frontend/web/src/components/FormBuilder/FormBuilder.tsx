// FormBuilder.tsx
import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Container,
  Button,
  Input,
  Select,
  Slider,
  Checkbox,
  NumberInput,
  InputWrapper,
  Stack,
  FileInput,
  MultiSelect,
  Group,
  Text,
  rem,
  useMantineTheme,
} from '@mantine/core';
import { Dropzone, MIME_TYPES } from '@mantine/dropzone';
import { IconDownload, IconX, IconCloudUpload } from '@tabler/icons-react';
import classes from './FormBuilder.module.css';

export interface FormField {
  type:
    | 'input'
    | 'button'
    | 'slider'
    | 'checkbox'
    | 'numberInput'
    | 'select'
    | 'fileInput'
    | 'dropzone'
    | 'multiSelect';
  id: string;
  label: string;
  // Additional properties based on the control type
  // For example, options for select, min/max for number input, etc.
  min?: number;
  max?: number;
  step?: number;
  allowNegative?: boolean;
  allowDecimal?: boolean;
  allowDeselect?: boolean;
  options?: { label: string; value: string }[];
  required?: boolean;
  description?: string;
  placeholder?: string;
  defaultValue?: string | null;
  onClick?: () => void;
  maxSize?: number;
  acceptedMIME?: string[];
  [key: string]: any;
}

interface FormBuilderProps {
  formFields: FormField[];
  data: {};
  onAutoSubmit: (formData: { [key: string]: any }) => void;
}

const FormBuilder: React.FC<FormBuilderProps> = ({
  formFields,
  data,
  onAutoSubmit,
}: FormBuilderProps) => {
  const theme = useMantineTheme();
  const openRef = useRef<() => void>(null);
  const [formData, setFormData] = useState<{ [key: string]: any }>(data);

  useEffect(() => {
    setFormData(data);
  }, [data]);

  const handleChange = useMemo(
    () => (id: string, value: any) => {
      const updatedFormData = { ...formData, [id]: value };
      setFormData(updatedFormData);
      onAutoSubmit(updatedFormData);
      // console.log(updatedFormData);
    },
    [formData, onAutoSubmit]
  );

  return (
    <Container>
      <Stack>
        {formFields.map((field) => (
          <React.Fragment key={`${field.type}_${field.id}`}>
            {field.type === 'input' && (
              <InputWrapper
                id={field.id}
                label={field.label}
                required={field.required}
                placeholder={field.placeholder}
                description={field.description}
              >
                <Input
                  value={formData[field.id] || ''}
                  onChange={(event) => handleChange(field.id, event.currentTarget.value)}
                />
              </InputWrapper>
            )}

            {field.type === 'button' && (
              <Button id={field.id} onClick={field.onClick}>
                {field.label}
              </Button>
            )}

            {field.type === 'slider' && (
              <Slider
                id={field.id}
                label={field.label}
                value={formData[field.id] || field.min}
                onChange={(value) => handleChange(field.id, value)}
                min={field.min}
                max={field.max}
                step={field.step}
              />
            )}

            {field.type === 'checkbox' && (
              <Checkbox
                id={field.id}
                label={field.label}
                checked={formData[field.id] || false}
                required={field.required}
                onChange={(event) => handleChange(field.id, event.currentTarget.checked as boolean)}
              />
            )}

            {field.type === 'numberInput' && (
              <InputWrapper id={field.id} label={field.label}>
                <NumberInput
                  value={field.min}
                  onChange={(value) => handleChange(field.id, value)}
                  min={field.min}
                  max={field.max}
                  step={field.step}
                  allowDecimal={field.allowDecimal}
                  allowNegative={field.allowNegative}
                  required={field.required}
                  placeholder={field.placeholder}
                  description={field.description}
                />
              </InputWrapper>
            )}

            {field.type === 'select' && field.options && (
              <Select
                id={field.id}
                label={field.label}
                onChange={(value) => handleChange(field.id, value)}
                data={field.options}
                placeholder={field.placeholder}
                defaultValue={field.defaultValue}
                allowDeselect={field.allowDeselect}
              />
            )}

            {field.type === 'multiSelect' && field.options && (
              <MultiSelect
                id={field.id}
                label={field.label}
                onChange={(value) => handleChange(field.id, value)}
                data={field.options}
                placeholder={field.placeholder}
              />
            )}

            {field.type === 'fileInput' && (
              <InputWrapper
                id={field.id}
                label={field.label}
                required={field.required}
                placeholder={field.placeholder}
                description={field.description}
              >
                <FileInput
                  value={formData[field.id] || null}
                  onChange={(value) => handleChange(field.id, value)}
                />
              </InputWrapper>
            )}

            {field.type === 'dropzone' && (
              <div className={classes.wrapper}>
                <Dropzone
                  id={field.id}
                  openRef={openRef}
                  onDrop={(value) => handleChange(field.id, value[0])}
                  className={classes.dropzone}
                  radius="md"
                  accept={field.acceptedMIME}
                  maxSize={field.maxSize}
                  multiple={false}
                >
                  <div style={{ pointerEvents: 'none' }}>
                    <Group justify="center">
                      <Dropzone.Accept>
                        <IconDownload
                          style={{ width: rem(50), height: rem(50) }}
                          color={theme.colors.blue[6]}
                          stroke={1.5}
                        />
                      </Dropzone.Accept>
                      <Dropzone.Reject>
                        <IconX
                          style={{ width: rem(50), height: rem(50) }}
                          color={theme.colors.red[6]}
                          stroke={1.5}
                        />
                      </Dropzone.Reject>
                      <Dropzone.Idle>
                        <IconCloudUpload style={{ width: rem(50), height: rem(50) }} stroke={1.5} />
                      </Dropzone.Idle>
                    </Group>

                    <Text ta="center" fw={700} fz="lg" mt="xl">
                      <Dropzone.Accept>Drop files here</Dropzone.Accept>
                      <Dropzone.Reject>Invalid file type</Dropzone.Reject>
                      <Dropzone.Idle>Upload file</Dropzone.Idle>
                    </Text>
                    <Text ta="center" fz="sm" mt="xs" c="dimmed">
                      Drag&apos;n&apos;drop files here to upload.
                    </Text>
                  </div>
                </Dropzone>

                <Button
                  className={classes.control}
                  size="md"
                  radius="xl"
                  onClick={() => openRef.current?.()}
                >
                  Select a file
                </Button>
              </div>
            )}
          </React.Fragment>
        ))}
      </Stack>
    </Container>
  );
};

export default React.memo(FormBuilder);
