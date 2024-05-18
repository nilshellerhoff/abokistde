<template>
  <span v-if="channelId">
    <ChannelPageHeader v-if="channel" :channel="channel" />
    <LoadingIndicator
      v-if="!hasUpdatedChannelEpisodes"
      style="width: 40px"
      class="q-mx-auto q-my-lg"
    />
    <EpisodeList
      v-else
      :showChannelHeader="false"
      :episode-api-params="episodeApiParams"
    />
  </span>
</template>

<script setup lang="ts">
import { apiClient } from 'src/util/api';
import { Ref, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { PublishingChannel } from 'src/types/api';
import ChannelPageHeader from 'components/ChannelPageHeader.vue';
import EpisodeList from 'components/EpisodeList/EpisodeList.vue';
import LoadingIndicator from 'components/LoadingIndicator.vue';

const route = useRoute();

const channelId = ref(route.params.id);
const channel: Ref<PublishingChannel | null> = ref(null);
const episodeApiParams = ref({
  publishing_channel_id: channelId.value,
});

const hasUpdatedChannelEpisodes = ref(false);

const updateChannelEpisodes = () => {
  apiClient
    .post(`/publishing_channel/${channelId.value}/update_episodes/`)
    .then(() => {
      episodeApiParams.value = {
        publishing_channel_id: route.params.id,
      };
      hasUpdatedChannelEpisodes.value = true;
    });
};

const getChannelInformation = () => {
  apiClient
    .get(`/publishing_channel/${route.params.id}/`)
    .then((response) => {
      console.log(response.data);
      channel.value = response.data;
    })
    .finally(() => {
      // isLoading.value--;
    });
};

watch(
  () => route.params.id,
  () => {
    getChannelInformation();
    updateChannelEpisodes();
  },
  { immediate: true }
);
</script>
