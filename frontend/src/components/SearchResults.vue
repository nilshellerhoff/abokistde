<template>
  <q-list style="max-width: 800px" class="q-mx-auto">
    <q-item v-for="result in searchResults" :key="result.id">
      <q-item-section>
        <channel-renderer
          :channel="result"
          :show-add-subscription="!isSubscribed(result.id)"
        />
      </q-item-section>
    </q-item>
    <q-item v-if="isSearching || isSearchingOnline" class="q-pa-md">
      <loading-indicator style="width: 40px" />
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

const contentStore = useContentStore();

interface Props {
  searchValue: string;
}

const props = defineProps<Props>();

const searchResults: Ref<any[]> = ref([]);
const isSearching = ref(false);
const isSearchingOnline = ref(false);

const search = () => {
  const currSearchValue = props.searchValue;
  if (props.searchValue.trim() !== '') {
    isSearching.value = true;
    apiClient
      .get('/publishing_channel/', {
        params: {
          search: props.searchValue.trim(),
        },
      })
      .then((response) => {
        if (currSearchValue !== props.searchValue) {
          return;
        }

        searchResults.value = response.data.results;
      })
      .finally(() => {
        isSearching.value = false;
      });
  }
};

const searchOnline = () => {
  const currSearchValue = props.searchValue;
  if (props.searchValue.trim() !== '') {
    isSearchingOnline.value = true;
    apiClient
      .get('/search_online/', {
        params: {
          query: props.searchValue.trim(),
        },
      })
      .then((response) => {
        if (currSearchValue !== props.searchValue) {
          return;
        }
        searchResults.value = uniqOn(
          [...searchResults.value, ...response.data.data],
          'id'
        );
      })
      .finally(() => {
        isSearchingOnline.value = false;
      });
  }
};

watch(
  () => props.searchValue,
  () => {
    searchResults.value = [];
    search();
    searchOnline();
  }
);

const isSubscribed = (channelId: number) => {
  return contentStore.subscriptions.some(
    (s) => s.publishing_channel.id === channelId
  );
};

search();
searchOnline();
</script>
