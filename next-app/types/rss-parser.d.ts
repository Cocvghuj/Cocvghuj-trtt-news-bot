declare module "rss-parser" {
  type FeedEntry = {
    title?: string;
    link?: string;
    isoDate?: string;
    pubDate?: string;
    guid?: string;
  };
  type Feed = { items?: FeedEntry[] };
  export default class Parser {
    constructor(options?: { timeout?: number; headers?: Record<string, string> });
    parseString(xml: string): Promise<Feed>;
  }
}
