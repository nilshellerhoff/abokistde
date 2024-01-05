<template>
  <q-item clickable :to="`/channel/${channel.id}`">
    <q-item-section avatar>
      <q-avatar>
        <q-img :src="channel.thumbnail_url">
          <template v-slot:error>
            <q-icon name="person" />
          </template>
        </q-img>
      </q-avatar>
    </q-item-section>
    <q-item-section>
      <q-item-label overline>
        {{ channel.provider.name }}
      </q-item-label>
      <q-item-label lines="1">
        {{ channel.name }}
      </q-item-label>
    </q-item-section>
    <q-item-section side>
      <q-btn
        v-if="showRemoveSubscription"
        flat
        round
        dense
        icon="delete"
        @click.prevent="$emit('unsubscribe', subscription)"
      />
      <q-btn
        v-if="showAddSubscription"
        flat
        round
        dense
        icon="add"
        @click.prevent="$emit('subscribe', channel)"
      />
    </q-item-section>
  </q-item>
</template>

<script setup lang="ts">
import { PublishingChannel, UserSubscription } from 'src/types/api';

interface Props {
  subscription?: UserSubscription;
  channel?: PublishingChannel;
  showRemoveSubscription?: boolean;
  showAddSubscription?: boolean;
}

const props = defineProps<Props>();

const channel = props.channel ?? props.subscription?.publishing_channel;
</script>
