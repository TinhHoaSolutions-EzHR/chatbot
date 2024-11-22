import "@/styles/globals.css";
import type {AppProps} from "next/app";
import "swagger-ui-react/swagger-ui.css";

export default function App({Component, pageProps}: AppProps) {
    return (
            <Component {...pageProps} />
    );
}
