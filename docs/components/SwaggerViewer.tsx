import dynamic from "next/dynamic";

// Dynamically import SwaggerUI to avoid SSR issues
const SwaggerUI = dynamic(() => import("swagger-ui-react"), { ssr: false });

import "swagger-ui-react/swagger-ui.css";

const SwaggerViewer = () => {
    return <SwaggerUI url="/assets/api-docs/openapi.yaml" />;
};

export default SwaggerViewer;
