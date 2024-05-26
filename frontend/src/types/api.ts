// -------- Generic -------- //
export type GenericPaginationResponse<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export type Primitive = string | number | null;

export type GenericUpdate<T> = Omit<Extract<T, Primitive>, 'id'>;

// --------- Provider -------- //

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

// -------- Episode --------- //
export type EpisodeModel = {
  id: number;
  title: string;
  description: string;
  thumbnail_url: string;
  url: string;
  published: string;
};

export type Episode = EpisodeModel & {
  is_hidden: boolean;
  is_favorited: boolean;
  publishing_channel: PublishingChannel;
};

export type EpisodeResponse = GenericPaginationResponse<Episode>;

// -------- Subscription --------- //
export type UserSubscriptionModel = {
  id: number;
  publishing_channel_id: number;
  category_id: number | null;
};

export type UserSubscription = UserSubscriptionModel & {
  publishing_channel: PublishingChannel;
  category: SubscriptionCategory | null;
};

// export type UserSubscriptionUpdate = GenericUpdate<UserSubscriptionModel>;
export type UserSubscriptionUpdate = Omit<UserSubscriptionModel, 'id'>;

// -------- Subscription Category --------- //
export type SubscriptionCategory = {
  name: string;
  icon: string;
  id: number;
};

export type SubscriptionCategoryResponse =
  GenericPaginationResponse<SubscriptionCategory>;

// -------- Search -------- //
export type SearchOnlineResponse = {
  data: {
    channels: PublishingChannel[];
    episodes: Episode[];
  };
};
