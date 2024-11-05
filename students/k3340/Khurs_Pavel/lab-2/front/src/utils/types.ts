import { IncomingMessage } from "http";

import { SVGProps } from "react";
import { NextPageContext } from "next";

export type IconSvgProps = SVGProps<SVGSVGElement> & {
  size?: number;
};

export interface CookieMessage extends IncomingMessage {
  cookies: { [name: string]: string };
}

export interface CookiesPageContext extends NextPageContext {
  req: CookieMessage | undefined;
}
