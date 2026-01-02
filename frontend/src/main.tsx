import { createRoot } from "react-dom/client";
import { LoginTest } from "./components/LoginTest.tsx";
import { Toaster } from "sonner";
import "./index.css";

createRoot(document.getElementById("root")!).render(
  <>
    <LoginTest />
    <Toaster />
  </>
);
