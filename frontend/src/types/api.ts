export type GenericPaginationResponse<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export type Provider = {
  id: number;
  name: string;
  url: string;
  icon_url: string;
};

export type ProviderResponse = GenericPaginationResponse<Provider>;

export type PublishingChannel = {
  id: number;
  name: string;
  url: string;
  description: string;
  thumbnail_url: string;
  provider: Provider;
};

export type PublishingChannelResponse =
  GenericPaginationResponse<PublishingChannel>;

export type UserSubscription = {
  id: number;
  publishing_channel: PublishingChannel;
};

export type Episode = {
  id: number;
  title: string;
  description: string;
  thumbnail_url: string;
  url: string;
  published: string;
  is_hidden: boolean;
  is_favorited: boolean;
  publishing_channel: PublishingChannel;
};

export type EpisodeResponse = GenericPaginationResponse<Episode>;
