import { PersonasTable } from "./PersonaTable";
import { FiPlusSquare } from "react-icons/fi";
import Link from "next/link";
import Text from "@/components/ui/text";
import Title from "@/components/ui/title";
import { Separator } from "@/components/ui/separator";
import { AssistantsIcon, RobotIcon } from "@/components/icons/icons";
import { AdminPageTitle } from "@/components/admin/Title";
import { ErrorCallout } from "@/components/ErrorCallout";
import { AssistantEditor } from "./AssistantEditor";
import { BackButton } from "@/components/BackButton";
import { DeletePersonaButton } from "./DeletePersonaButton";
import { fetchAssistantEditorInfoSS } from "@/lib/assistants/fetchPersonaEditorInfoSS";
import { SuccessfulPersonaUpdateRedirectType } from "./enums";
import CardSection from "@/components/admin/CardSection";

export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ id: string | null }>;
}) {
  const { id } = await searchParams;
  if (!id) {
    return (
      <div className="mx-auto container">
        <AdminPageTitle
          icon={<AssistantsIcon size={32} />}
          title="Assistants"
        />

        <Text className="mb-2">
          Assistants are a way to build custom search/question-answering
          experiences for different use cases.
        </Text>
        <Text className="mt-2">They allow you to customize:</Text>
        <div className="text-sm">
          <ul className="list-disc mt-2 ml-4">
            <li>
              The prompt used by your LLM of choice to respond to the user query
            </li>
            <li>The documents that are used as context</li>
          </ul>
        </div>

        <div>
          <Separator />

          <Title>Create an Assistant</Title>
          <Link
            href="/admin/assistants/new"
            className="flex py-2 px-4 mt-2 border border-border h-fit cursor-pointer hover:bg-hover text-sm w-40"
          >
            <div className="mx-auto flex">
              <FiPlusSquare className="my-auto mr-2" />
              New Assistant
            </div>
          </Link>

          <Separator />

          <Title>Existing Assistants</Title>
          <PersonasTable />
        </div>
      </div>
    );
  } else {
    const [values, error] = await fetchAssistantEditorInfoSS(id);
    let body;
    if (!values) {
      body = (
        <ErrorCallout errorTitle="Something went wrong :(" errorMsg={error} />
      );
    } else {
      body = (
        <>
          <CardSection>
            <AssistantEditor
              {...values}
              admin
              defaultPublic={true}
              redirectType={SuccessfulPersonaUpdateRedirectType.ADMIN}
            />
          </CardSection>

          <div className="mt-12">
            <Title>Delete Assistant</Title>

            <div className="flex mt-6">
              <DeletePersonaButton
                personaId={values.existingPersona!.id}
                redirectType={SuccessfulPersonaUpdateRedirectType.ADMIN}
              />
            </div>
          </div>
        </>
      );
    }

    return (
      <div className="w-full">
        <BackButton />
        <AdminPageTitle title="Edit Assistant" icon={<RobotIcon size={32} />} />
        {body}
      </div>
    );
  }
}
