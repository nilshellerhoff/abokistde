<template>
  <q-list
    style="width: 100%; max-width: 800px"
    class="q-mx-auto q-my-lg q-pa-sm"
  >
    <q-input
      v-model="query"
      style="width: 100%"
      placeholder="Search..."
      autofocus
    >
      <template #prepend>
        <q-icon name="search" />
      </template>
    </q-input>

    <div v-if="query !== ''">
      <q-tabs v-model="tab" class="text-teal">
        <q-tab name="channels" label="Channels" />
        <q-tab name="episodes" label="Episodes" />
      </q-tabs>

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="channels">
          <SearchContentChannels :channels="channels" />
        </q-tab-panel>

        <q-tab-panel name="episodes">
          <SearchContentEpisodes :episodes="episodes" />
        </q-tab-panel>
      </q-tab-panels>

      <q-item
        v-if="Object.values(isSearching).some((e) => e.value)"
        class="q-pa-md"
      >
        <div style="width: 100%">
          <loading-indicator style="width: 40px" class="q-mx-auto" />
        </div>
      </q-item>
    </div>
  </q-list>
</template>

<script lang="ts" setup>
import { apiClient } from 'src/util/api';
import { ref, watch } from 'vue';
import LoadingIndicator from 'components/LoadingIndicator.vue';
import { uniqOn } from 'src/util/array';
import { useContentStore } from 'stores/content-store';
import { watchDebounced } from '@vueuse/core';
import SearchContentChannels from 'components/Search/SearchContentChannels.vue';
import {
  Episode,
  PublishingChannel,
  SearchOnlineResponse,
} from 'src/types/api';
import SearchContentEpisodes from 'components/Search/SearchContentEpisodes.vue';

const contentStore = useContentStore();

const query = ref('');
const channels = ref<PublishingChannel[]>([]);
const episodes = ref<Episode[]>([]);

const isSearching = {
  channelsApi: ref(false),
  episodesApi: ref(false),
  online: ref(false),
};

const tab = ref('channels');

const mergeSearchResults = (a: any[], b: any[]): any[] => {
  return uniqOn([...a, ...b], 'id');
};

const searchStore = () => {
  if (query.value.trim() !== '') {
    const subscriptions = contentStore.subscriptions.filter((c) =>
      c.publishing_channel.name
        .toLowerCase()
        .includes(query.value.trim().toLowerCase())
    );
    channels.value = mergeSearchResults(
      channels.value,
      subscriptions.map((s) => s.publishing_channel)
    );
  }
};

const searchApi = () => {
  const currSearchValue = query.value;
  if (query.value.trim() !== '') {
    isSearching.channelsApi.value = true;

    apiClient
      .get('/publishing_channel/', {
        params: {
          search: query.value.trim(),
        },
      })
      .then((response) => {
        if (currSearchValue !== query.value) {
          return;
        }
        channels.value = mergeSearchResults(
          channels.value,
          response.data.results
        );
      })
      .finally(() => {
        isSearching.channelsApi.value = false;
      });
  }
};

const searchOnline = () => {
  const currSearchValue = query.value;
  if (query.value.trim() !== '') {
    isSearching.online.value = true;
    apiClient
      .get<SearchOnlineResponse>('/search_online/', {
        params: {
          query: query.value.trim(),
        },
      })
      .then((response) => {
        if (currSearchValue !== query.value) {
          return;
        }
        channels.value = mergeSearchResults(
          channels.value,
          response.data.data.channels
        );

        episodes.value = mergeSearchResults(
          episodes.value,
          response.data.data.episodes
        );
      })
      .finally(() => {
        isSearching.online.value = false;
      });
  }
};

watch(
  () => query.value,
  () => {
    channels.value = [];
    episodes.value = [];
    searchStore();
  }
);

watchDebounced(
  () => query.value,
  () => {
    searchApi();
    searchOnline();
  },
  { debounce: 500 }
);

searchApi();
searchOnline();
</script>
