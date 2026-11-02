export type BBox = {
  x: number;
  y: number;
  w: number;
  h: number;
  label?: string;
  confidence?: number;
};

export type Detection = {
  label: string;
  confidence: number;
  x?: number;
  y?: number;
  w?: number;
  h?: number;
};

export type BBoxVerdict = {
  index: number;
  verdict: "false_alarm" | "confirm" | "uncertain" | string;
  reason: string;
  alarm_bbox?: BBox;
  center?: { x: number; y: number };
};

export type TaskSummary = {
  task_id: string;
  created_at: string | null;
  status: string;
  source: string;
};

export type TaskDetail = TaskSummary & {
  alarm_id?: string | null;
  alarm_bboxes: BBox[];
  detections: Detection[];
  cabin_bboxes?: BBox[];
  bbox_verdicts?: BBoxVerdict[];
  image_url: string;
  error?: string | null;
};
