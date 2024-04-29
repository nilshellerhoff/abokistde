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

    <channel-renderer
      v-for="result in searchResults"
      :key="result.id"
      :channel="result"
      :show-add-subscription="!isSubscribed(result.id)"
    />
    <q-item v-if="isSearchingApi || isSearchingOnline" class="q-pa-md">
      <div style="width: 100%">
        <loading-indicator style="width: 40px" class="q-mx-auto" />
      </div>
    </q-item>
  </q-list>
</template>

<script lang="ts" setup>
import { apiClient } from 'src/util/api';
import { Ref, ref, watch } from 'vue';
import LoadingIndicator from 'components/LoadingIndicator.vue';
import ChannelRenderer from 'components/ChannelRenderer.vue';
import { uniqOn } from 'src/util/array';
import { useContentStore } from 'stores/content-store';
import { watchDebounced } from '@vueuse/core';

const contentStore = useContentStore();

const query = ref('');
const searchResults: Ref<any[]> = ref([]);
const isSearchingApi = ref(false);
const isSearchingOnline = ref(false);

const mergeSearchResults = (a: any[], b: any[]) => {
  return uniqOn([...a, ...b], 'id');
};

const searchStore = () => {
  if (query.value.trim() !== '') {
    const subscriptions = contentStore.subscriptions.filter((c) =>
      c.publishing_channel.name
        .toLowerCase()
        .includes(query.value.trim().toLowerCase())
    );
    searchResults.value = mergeSearchResults(
      searchResults.value,
      subscriptions.map((s) => s.publishing_channel)
    );
  }
};

const searchApi = () => {
  const currSearchValue = query.value;
  if (query.value.trim() !== '') {
    isSearchingApi.value = true;
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
        searchResults.value = mergeSearchResults(
          searchResults.value,
          response.data.results
        );
      })
      .finally(() => {
        isSearchingApi.value = false;
      });
  }
};

const searchOnline = () => {
  const currSearchValue = query.value;
  if (query.value.trim() !== '') {
    isSearchingOnline.value = true;
    apiClient
      .get('/search_online/', {
        params: {
          query: query.value.trim(),
        },
      })
      .then((response) => {
        if (currSearchValue !== query.value) {
          return;
        }
        searchResults.value = mergeSearchResults(
          searchResults.value,
          response.data.data
        );
      })
      .finally(() => {
        isSearchingOnline.value = false;
      });
  }
};

const isSubscribed = (channelId: number) => {
  return contentStore.subscriptions.some(
    (s) => s.publishing_channel.id === channelId
  );
};

watch(
  () => query.value,
  () => {
    searchResults.value = [];
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
