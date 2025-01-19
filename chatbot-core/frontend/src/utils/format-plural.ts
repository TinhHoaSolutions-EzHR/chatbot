interface FormatPluralOptions {
  customPlural?: string;
  pluralEnd?: string;
}

const DEFAULT_PLURAL_END = 's';

export const formatPlural = (amount: number, word: string, options?: FormatPluralOptions) => {
  const pluralEnd = options?.pluralEnd ?? DEFAULT_PLURAL_END;

  if (amount === 1) {
    return word;
  }

  return options?.customPlural ?? `${word}${pluralEnd}`;
};
