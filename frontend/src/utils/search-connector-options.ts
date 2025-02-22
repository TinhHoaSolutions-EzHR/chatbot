import { ADMIN_CONNECTOR_OPTIONS, IAdminConnectorOption } from '@/constants/admin-connector-options';

export const searchConnectorOptions = (searchValue: string) => {
  if (!searchValue) {
    return ADMIN_CONNECTOR_OPTIONS;
  }

  const cleanedSearchValue = searchValue.trim().toLowerCase();

  return ADMIN_CONNECTOR_OPTIONS.reduce<IAdminConnectorOption[]>((acc, cur) => {
    if (cur.title.toLowerCase().includes(cleanedSearchValue)) {
      acc.push(cur);
      return acc;
    }

    const matchingConnectors = cur.connectors.filter(connector =>
      connector.name.toLowerCase().includes(cleanedSearchValue),
    );

    if (!matchingConnectors.length) {
      return acc;
    }

    const filteredConnectorOption: IAdminConnectorOption = {
      ...cur,
      connectors: matchingConnectors,
    };

    acc.push(filteredConnectorOption);

    return acc;
  }, []);
};
