export const uniq = <T>(arr: T[]): T[] => [...new Set(arr)];

export const uniqOn = <T>(
  arr: (Record<string | number, T> | null)[],
  key: string
): (Record<string | number, T> | null)[] => {
  const uniqIds = uniq(arr.map((e) => e?.[key]));
  return uniqIds.map((id) =>
    id ? arr.find((e) => e?.[key] === id) ?? null : null
  );
};
