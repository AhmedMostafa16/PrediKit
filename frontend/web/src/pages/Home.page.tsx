import { Button, Center } from '@mantine/core';
import { Link } from 'react-router-dom';
import { HeaderMegaMenu } from '@/components/HeaderMegaMenu/HeaderMegaMenu';

export default function Home() {
  return (
    <>
      <HeaderMegaMenu />
      <Center>
        <Button component={Link} to="/workflows">
          Go to Workflow Designer
        </Button>
      </Center>
    </>
  );
}
