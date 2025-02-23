export interface IApiResponse<T> {
  message: string;
  headers: string | null;
  data: T;
}
