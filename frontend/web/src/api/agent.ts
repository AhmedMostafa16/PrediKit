import axios, { AxiosResponse } from 'axios';
import { Workflow, CreateWorkflowDto, UpdateWorkflowDto } from '@/models/Workflow';
import { Path } from '@/types/Path';

axios.defaults.baseURL = 'http://localhost:5000/api';
// axios.defaults.headers.common['Accept-Encoding'] = 'gzip, br, deflate'; // EXPERIMENTAL

const responseBody = (response: AxiosResponse) => response.data;

const requests = {
  get: <T>(url: string) => axios.get<T>(url).then(responseBody),
  post: <T>(url: string, body: object) => axios.post<T>(url, body).then(responseBody),
  put: <T>(url: string, body: object) => axios.put<T>(url, body).then(responseBody),
  delete: <T>(url: string) => axios.delete<T>(url).then(responseBody),
};

const Workflows = {
  list: () => requests.get<Workflow[]>('/workflows'),
  details: (id: string) => requests.get<Workflow>(`/workflows/${id}`),
  create: (workflow: CreateWorkflowDto) => requests.post<void>('/workflows/', workflow),
  update: (workflow: UpdateWorkflowDto) =>
    requests.put<void>(`/workflows/${workflow.id}`, workflow),
  delete: (id: string) => requests.delete<void>(`/workflows/${id}`),
  execute: (id: string) => requests.post<void>(`/workflows/${id}/execute`, {}),
  executePaths: (id: string, paths: Path[]) =>
    requests.post<void>(`/workflows/${id}/execute`, paths),
  listColumnNames: (id: string) => requests.get<string[]>(`/workflows/${id}/get_columns_names`),
};

const agent = {
  Workflows,
};

export default agent;
