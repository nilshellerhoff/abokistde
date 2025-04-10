<template>
  <div class="row q-pa-lg">
    <q-btn flat icon="refresh" @click="loadEpisodes">
      <q-tooltip>Refresh</q-tooltip>
    </q-btn>
    <q-toggle
      v-model="showHidden"
      label="Show hidden"
      @update:model-value="loadEpisodes"
    />
    <q-space />
    <CardWidthSelector />
    <span>
      <q-input
        borderless
        dense
        hide-bottom-space
        style="width: 120px"
        readonly
        v-model="localSettingsStore.episodeListMaxNumberOfColumns"
      >
        <template #before> <q-icon name="view_column" /></template>
        <template #prepend>
          <q-btn icon="remove" flat dense @click="decreaseColumnNumber"></q-btn>
        </template>
        <template #append>
          <q-btn icon="add" flat dense @click="increaseColumnNumber"></q-btn>
        </template>
      </q-input>
      <q-tooltip>Maximum number of columns</q-tooltip>
    </span>
  </div>
  <div
    class="row items-start justify-center q-pa-sm q-mx-auto q-gutter-md episode-grid"
    :style="{ width: columnWrapperWidth + 'px', maxWidth: '100%' }"
  >
    <episode-list-item
      v-for="episode in shownEpisodes"
      :key="episode.id"
      :show-channel-header="props.showChannelHeader"
      :episode="episode"
      :width="episodeCardWidth"
      @hideUnhide="hideUnhideEpisode(episode)"
      @favorite="favoriteEpisode(episode)"
    />
  </div>
  <div v-if="!isLoading && (!episodes || !episodes.length)">
    <span class="text-h5">No episodes found.</span>
  </div>
  <div v-if="!isLoading">
    <div v-if="isEpisodesLeft">
      <q-btn
        style="display: block"
        class="q-mx-auto q-my-lg"
        @click="fetchEpisodes"
        color="primary"
      >
        <q-icon name="expand_more" />
        <span>load more</span>
      </q-btn>
    </div>
    <div v-else class="q-pa-lg text-center">
      No more episodes. More episodes might be found on the channel page(s).
    </div>
  </div>
  <div v-if="isLoading">
    <loading-indicator
      class="q-mx-auto q-my-lg"
      style="width: 40px"
    ></loading-indicator>
  </div>
</template>

<script setup lang="ts">
import { computed, Ref, ref, watch } from 'vue';
import EpisodeListItem from 'components/EpisodeList/EpisodeListItem.vue';
import { apiClient } from 'src/util/api';
import { Episode, EpisodeResponse } from 'src/types/api';
import LoadingIndicator from 'components/LoadingIndicator.vue';
import { objectsDiffer } from 'src/util/object';
import { useLocalSettingsStore } from 'stores/local-settings-store';
import CardWidthSelector from 'components/EpisodeList/CardWidthSelector.vue';
import { useQuasar } from 'quasar';

interface Props {
  episodeApiParams?: any; // TODO
  showChannelHeader?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showChannelHeader: true,
});
const $q = useQuasar();
const localSettingsStore = useLocalSettingsStore();

const isLoading = ref(0);
const currentOffset = ref(0);
const pageSize = ref(48);
const episodes: Ref<Episode[]> = ref([]);
const showHidden = ref(false);
const isEpisodesLeft = ref(true);

const shownEpisodes = computed(() => {
  if (showHidden.value) {
    return episodes.value;
  } else {
    return episodes.value.filter((e) => !e.is_hidden);
  }
});

const fetchEpisodes = () => {
  isLoading.value++;

  let query_params = { ...props.episodeApiParams } || {};

  query_params.offset = currentOffset.value;
  query_params.limit = pageSize.value;

  if (!showHidden.value) {
    query_params.is_hidden = false;
  }

  apiClient
    .get<EpisodeResponse>('/episode/', {
      params: query_params,
    })
    .then((response) => {
      episodes.value = [...episodes.value, ...response.data.results];
      currentOffset.value += pageSize.value;
      isEpisodesLeft.value = response.data.next !== null;
    })
    .finally(() => {
      isLoading.value--;
    });
};

const resetEpisodes = () => {
  episodes.value = [];
  currentOffset.value = 0;
};

const hideUnhideEpisode = (episode: Episode) => {
  const action = episode.is_hidden ? 'unhide' : 'hide';
  const undoAction = episode.is_hidden ? 'hide' : 'unhide';
  const message = episode.is_hidden ? 'Episode unhidden' : 'Episode hidden';

  const undoHandler = () => {
    apiClient.post(`/episode_user/${episode.id}/${undoAction}/`).then(() => {
      episode.is_hidden = !episode.is_hidden;
    });
  };

  apiClient.post(`/episode_user/${episode.id}/${action}/`).then(() => {
    episode.is_hidden = !episode.is_hidden;
    $q.notify({
      type: 'positive',
      message,
      actions: [
        {
          label: 'Undo',
          color: 'white',
          handler: undoHandler,
        },
      ],
    });
  });
};

const favoriteEpisode = (episode: Episode) => {
  const action = episode.is_favorited ? 'unfavorite' : 'favorite';
  apiClient.post(`/episode_user/${episode.id}/${action}/`).then(() => {
    episode.is_favorited = !episode.is_favorited;
  });
};

const loadEpisodes = () => {
  resetEpisodes();
  fetchEpisodes();
};

loadEpisodes();

watch(
  () => props.episodeApiParams,
  (newValue, oldValue) => {
    console.log('episodeApiParams changed');
    // somehow needed, scrolling on iPad otherwise triggered this watch
    if (objectsDiffer(newValue, oldValue)) {
      loadEpisodes();
    }
  },
  { deep: true }
);

const episodeCardWidth = computed(() => {
  return window.innerWidth >= 2 * localSettingsStore.episodeListEpisodeCardWidth
    ? localSettingsStore.episodeListEpisodeCardWidth
    : window.innerWidth;
});

const calculateColumnWrapperWidth = () =>
  localSettingsStore.episodeListMaxNumberOfColumns *
    (episodeCardWidth.value + 16) +
  16;

const columnWrapperWidth = ref(calculateColumnWrapperWidth());

const increaseColumnNumber = () => {
  localSettingsStore.episodeListMaxNumberOfColumns =
    localSettingsStore.episodeListMaxNumberOfColumns + 1;
  columnWrapperWidth.value = calculateColumnWrapperWidth();
};

const decreaseColumnNumber = () => {
  localSettingsStore.episodeListMaxNumberOfColumns =
    localSettingsStore.episodeListMaxNumberOfColumns - 1;
  columnWrapperWidth.value = calculateColumnWrapperWidth();
};
</script>

<style>
.episode-grid::after {
  content: '';
  flex: auto;
}
</style>
