import { AdminPageTitle } from "@/components/admin/Title";
import { FiBarChart2 } from "react-icons/fi";
import Text from "@/components/ui/text";
import { CustomAnalyticsUpdateForm } from "./CustomAnalyticsUpdateForm";

function Main() {
  return (
    <div>
      <Text className="mb-8">
        This allows you to bring your own analytics tool to Danswer! Copy the
        Web snippet from your analytics provider into the box below, and
        we&apos;ll start sending usage events.
      </Text>

      <CustomAnalyticsUpdateForm />
    </div>
  );
}

export default function Page() {
  return (
    <main className="pt-4 mx-auto container">
      <AdminPageTitle
        title="Custom Analytics"
        icon={<FiBarChart2 size={32} />}
      />

      <Main />
    </main>
  );
}
