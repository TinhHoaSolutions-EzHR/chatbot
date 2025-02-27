import { toast } from 'sonner';

class ToastService {
  static apiFail() {
    toast.error('Something went wrong', {
      description: "There's something wrong with your request. Please try again later.",
    });
  }
}

export default ToastService;
