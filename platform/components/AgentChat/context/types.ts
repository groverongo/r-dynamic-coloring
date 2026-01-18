import { Dispatch, SetStateAction } from "react";
import { CustomMessage } from "../content";

export type ChatContextType = {
  input: string;
  setInput: Dispatch<SetStateAction<string>>;
  messages: CustomMessage[];
  setMessages: Dispatch<SetStateAction<CustomMessage[]>>;
  isPending: boolean;
  callAgent: () => void;
}