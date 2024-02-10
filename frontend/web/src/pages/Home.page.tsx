import { Button, Center } from '@mantine/core';
import { Link } from 'react-router-dom';
import { LandingHeaderMegaMenu } from '@/components/LandingHeaderMegaMenu/LandingHeaderMegaMenu';

export default function Home() {
  return (
    <>
      <LandingHeaderMegaMenu />
      <Center>
        <Button component={Link} to="/workflows">
          Go to Workflow Designer
        </Button>
      </Center>
    </>
  );
}
