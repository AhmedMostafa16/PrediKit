/* eslint-disable @typescript-eslint/no-explicit-any */
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
  ComboboxData,
} from '@mantine/core';
import { Dropzone, FileWithPath } from '@mantine/dropzone';
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
  options?: ComboboxData | (() => ComboboxData);
  required?: boolean;
  description?: string;
  placeholder?: string;
  defaultValue?: number | string | null;
  defaultChecked?: boolean;
  searchable?: boolean;
  onClick?: () => void;
  maxSize?: number;
  acceptedMIME?: string[];
  dependencies?: {
    fieldId: string; // The ID of the dependent field
    triggerValue: any; // The value that triggers the dependency
    optional: boolean; // If true, the dependency is optional
  }[];
  [key: string]: any;
}

interface FormBuilderProps {
  formFields: FormField[];
  data: any;
  onAutoSubmit: (formData: { [key: string]: any }) => void;
}

const FormBuilder: React.FC<FormBuilderProps> = ({
  formFields,
  data,
  onAutoSubmit,
}: FormBuilderProps) => {
  const theme = useMantineTheme();
  const openRef = useRef<() => void>(null);
  const [formFieldsData, setFormData] = useState<{ [key: string]: any }>(data);

  useEffect(() => {
    setFormData(data);
  }, [data, formFields]);

  const handleChange = useMemo(
    () => (id: string, value: any) => {
      const updatedFormData = { ...formFieldsData, [id]: value };
      setFormData(updatedFormData);
      onAutoSubmit(updatedFormData);
      // console.log(updatedFormData);
    },
    [formFieldsData, onAutoSubmit]
  );

  const shouldRenderField = (field: FormField) => {
    if (!field.dependencies) {
      return true;
    }

    for (const dependency of field.dependencies) {
      const dependentFieldValue = formFieldsData[dependency.fieldId];
      if (dependentFieldValue !== dependency.triggerValue && !dependency.optional) {
        return false;
      }
    }

    return true;
  };

  return (
    <Container>
      <Stack>
        {formFields.map(
          (field) =>
            shouldRenderField(field) && (
              <React.Fragment key={`${field.type}_${field.id}`}>
                {field.type === 'input' && (
                  <InputWrapper
                    id={field.id}
                    label={field.label}
                    required={field.required}
                    description={field.description}
                  >
                    <Input
                      value={formFieldsData[field.id] || field.defaultValue || ''}
                      placeholder={field.placeholder}
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
                    value={formFieldsData[field.id] || field.min}
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
                    checked={formFieldsData[field.id] || false}
                    required={field.required}
                    onChange={(event) =>
                      handleChange(field.id, event.currentTarget.checked as boolean)
                    }
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
                    data={
                      typeof field.options === 'function'
                        ? field.options()
                        : (field.options as ComboboxData)
                    }
                    placeholder={field.placeholder}
                    defaultValue={String(field.defaultValue)}
                    value={formFieldsData[field.id]}
                    multiple={false}
                    allowDeselect={field.allowDeselect}
                    onLoad={field.onLoad}
                    searchable={field.searchable}
                  />
                )}

                {field.type === 'multiSelect' && field.options && (
                  <MultiSelect
                    id={field.id}
                    label={field.label}
                    onChange={(value) => handleChange(field.id, value)}
                    data={
                      typeof field.options === 'function'
                        ? field.options()
                        : (field.options as ComboboxData)
                    }
                    value={formFieldsData[field.id]}
                    placeholder={field.placeholder}
                  />
                )}

                {field.type === 'fileInput' && (
                  <InputWrapper
                    id={field.id}
                    label={field.label}
                    required={field.required}
                    description={field.description}
                  >
                    <FileInput
                      value={formFieldsData[field.id] || null}
                      onChange={(value) => handleChange(field.id, value)}
                    />
                  </InputWrapper>
                )}

                {field.type === 'dropzone' && (
                  <div className={classes.wrapper}>
                    <Dropzone
                      id={field.id}
                      openRef={openRef}
                      onDrop={async (value: FileWithPath[]) => {
                        const file = value[0];
                        return handleChange(field.id, file);
                      }}
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
                            <IconCloudUpload
                              style={{ width: rem(50), height: rem(50) }}
                              stroke={1.5}
                            />
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
            )
        )}
      </Stack>
    </Container>
  );
};

export default FormBuilder;
