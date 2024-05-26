<template>
  <div v-if="props.channels.length == 0">
    <q-item>
      <q-item-section>
        <q-item-label>No episodes found</q-item-label>
      </q-item-section>
    </q-item>
  </div>
  <channel-renderer
    v-for="channel in props.channels"
    :key="channel.id"
    :channel="channel"
    :show-add-subscription="!isSubscribed(channel.id)"
  />
</template>
<script setup lang="ts">
import ChannelRenderer from 'components/ChannelRenderer.vue';
import { useContentStore } from 'stores/content-store';
import { PublishingChannel } from 'src/types/api';

interface Props {
  channels: PublishingChannel[];
}

const props = defineProps<Props>();

const contentStore = useContentStore();

const isSubscribed = (channelId: number) => {
  return contentStore.subscriptions.some(
    (s) => s.publishing_channel.id === channelId
  );
};
</script>
