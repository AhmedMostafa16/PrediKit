import { Card, Center, Text } from '@mantine/core';
import React from 'react';
import { Handle, Position } from 'reactflow';
import { BaseNode } from '../../nodes/BaseNode';

export default function NodeFactory(props: BaseNode) {
  // console.log(props.inputHandles.length);
  // console.log(props.outputHandles.length);

  const node = () => (
    <div>
      <Card style={{ background: `var(--mantine-color-${props.color}-6)` }} padding="sm">
        <Center inline>
          {React.cloneElement(props.icon, {
            size: 40,
            style: {
              color: `var(--mantine-color-${props.color}-0)`,
              margin: 0,
              padding: 0,
            },
          })}
        </Center>
      </Card>
      <Text size="xs" ta="center" style={{ padding: 0, maxWidth: 64 }}>
        {props.label}
      </Text>

      {props.inputHandles &&
        props.inputHandles.map((item, index) => (
          <Handle
            type="target"
            position={Position.Left}
            key={index}
            id={`t${index}`}
            onConnect={item.onConnect}
            isValidConnection={item.isValidConnection}
            style={{
              left: -16,
              top: 32 / props.inputHandles.length + (index * 64) / props.inputHandles.length,
              background: 'var(--mantine-color-gray-6)',
              borderColor: 'var(--mantine-color-gray-6)',
              borderRadius: '0 50% 50% 0',
              borderWidth: 4,
            }}
          />
        ))}
      {props.outputHandles &&
        props.outputHandles.map((item, index) => (
          <Handle
            type="source"
            position={Position.Right}
            key={index}
            id={`s${index}`}
            onConnect={item.onConnect}
            isValidConnection={item.isValidConnection}
            style={{
              right: -16,
              top: 32 / props.outputHandles.length + (index * 64) / props.outputHandles.length,
              background: 'var(--mantine-color-gray-6)',
              borderColor: 'var(--mantine-color-gray-6)',
              borderRadius: '0 50% 50% 0',
              borderWidth: 4,
            }}
          />
        ))}
    </div>
  );

  node.displayName = props.name;

  return node;
}
