"use client";

import { Button, Center } from "@mantine/core";
import Link from "next/link";
import { HeaderMegaMenu } from "./_components/HeaderMegaMenu/HeaderMegaMenu";

export default function Home() {
  return (
    <>
      <HeaderMegaMenu />
      <Center>
        <Button component={Link} href={"/workflows"}>
          Go to Workflow Designer
        </Button>
      </Center>
    </>
  );
}
